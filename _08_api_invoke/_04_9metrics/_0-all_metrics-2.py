import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplcursors

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplcursors
import glob

# --------------------------
# 1) 合成 high/low（只用 open/close）
# --------------------------
def add_synthetic_high_low(df, pct=0.002):
    df = df.copy()
    base_high = df[["open", "close"]].max(axis=1)
    base_low  = df[["open", "close"]].min(axis=1)
    df["high"] = base_high * (1 + pct)
    df["low"]  = base_low  * (1 - pct)
    return df

# --------------------------
# 2) 指标计算
# --------------------------
def compute_rsi(close, period=14):
    delta = close.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    ma_up = up.ewm(alpha=1/period, adjust=False).mean()
    ma_down = down.ewm(alpha=1/period, adjust=False).mean()
    rs = ma_up / (ma_down.replace(0, np.nan))
    rsi = 100 - 100/(1+rs)
    return rsi.fillna(50)

def compute_cci(high_like, low_like, close, n=20):
    tp = (high_like + low_like + close) / 3.0
    ma = tp.rolling(n, min_periods=1).mean()
    md = tp.rolling(n, min_periods=1).apply(lambda x: np.mean(np.abs(x - np.mean(x))), raw=True)
    cci = (tp - ma) / (0.015 * (md + 1e-9))
    return cci.fillna(0)

def compute_mfi(close, volume, n=14):
    if volume.isna().all():
        return pd.Series(np.nan, index=close.index)
    high_like = close.rolling(n, min_periods=1).max()
    low_like  = close.rolling(n, min_periods=1).min()
    tp = (high_like + low_like + close) / 3.0
    raw = tp * volume
    positive = []
    negative = []
    for i in range(1, len(tp)):
        if tp.iloc[i] > tp.iloc[i-1]:
            positive.append(raw.iloc[i]); negative.append(0.0)
        else:
            positive.append(0.0);    negative.append(raw.iloc[i])
    positive = [np.nan] + positive
    negative = [np.nan] + negative
    pos = pd.Series(positive, index=close.index).rolling(n, min_periods=1).sum()
    neg = pd.Series(negative, index=close.index).rolling(n, min_periods=1).sum()
    mfr = pos / (neg.replace(0, np.nan))
    mfi = 100 - (100 / (1 + mfr))
    return mfi.fillna(50)

def compute_bollinger_pctb(close, n=20, k=2):
    ma = close.rolling(n, min_periods=1).mean()
    std = close.rolling(n, min_periods=1).std()
    upper = ma + k * std
    lower = ma - k * std
    pb = (close - lower) / (upper - lower + 1e-9)
    return pb.fillna(0.5), upper, lower

def compute_kd(high_like, low_like, close, k_period=14, d_period=3):
    highest = high_like.rolling(k_period, min_periods=1).max()
    lowest  = low_like.rolling(k_period, min_periods=1).min()
    k = 100 * (close - lowest) / (highest - lowest + 1e-9)
    d = k.rolling(d_period, min_periods=1).mean()
    return k.fillna(50), d.fillna(50)

# --------------------------
# 3) 无未来 swing high/low（用于背离）
# --------------------------
def find_swings_no_lookahead(series):
    lows = []; highs = []
    arr = series.values
    for i in range(2, len(arr)):
        if arr[i] < arr[i-1] and arr[i] < arr[i-2]:
            lows.append(i)
        if arr[i] > arr[i-1] and arr[i] > arr[i-2]:
            highs.append(i)
    return np.array(lows, dtype=int), np.array(highs, dtype=int)

def detect_divergence_price_vs_indicator(price, indicator, swing_lows=None, swing_highs=None):
    if swing_lows is None or swing_highs is None:
        lows, highs = find_swings_no_lookahead(price)
    else:
        lows, highs = swing_lows, swing_highs
    bullish=[]; bearish=[]
    for i in range(1,len(lows)):
        p1,p2=lows[i-1],lows[i]
        if price.iloc[p2]<price.iloc[p1] and indicator.iloc[p2]>indicator.iloc[p1]:
            bullish.append(p2)
    for i in range(1,len(highs)):
        p1,p2=highs[i-1],highs[i]
        if price.iloc[p2]>price.iloc[p1] and indicator.iloc[p2]<indicator.iloc[p1]:
            bearish.append(p2)
    return np.array(bullish,dtype=int), np.array(bearish,dtype=int)

def detect_bollinger_reversal(pctb):
    tops=[]; bottoms=[]
    p=pctb.values
    for i in range(1,len(p)):
        if p[i-1]>1 and p[i]<=1: tops.append(i)
        if p[i-1]<0 and p[i]>=0: bottoms.append(i)
    return np.array(tops,dtype=int), np.array(bottoms,dtype=int)

def detect_kd_divergence(close,k):
    lows,highs=find_swings_no_lookahead(close)
    return detect_divergence_price_vs_indicator(close,k,lows,highs)

# --------------------------
# 4) 主流程
# --------------------------
def multi_indicator_signals(df):
    df = df.copy().reset_index(drop=True)
    df['date'] = pd.to_datetime(df['date'])
    df = add_synthetic_high_low(df, pct=0.002)
    close = df['close'].astype(float)

    df['rsi'] = compute_rsi(close)
    df['k'], df['d'] = compute_kd(df['high'], df['low'], close)
    df['cci'] = compute_cci(df['high'], df['low'], close)
    df['mfi'] = compute_mfi(close, df['volume'])
    df['pctb'], df['bb_upper'], df['bb_lower'] = compute_bollinger_pctb(close)

    lows, highs = find_swings_no_lookahead(close)

    signals = {'rsi':{'bull':[],'bear':[]},
               'cci':{'bull':[],'bear':[]},
               'mfi':{'bull':[],'bear':[]},
               'kd':{'bull':[],'bear':[]},
               'bollinger':{'top':[],'bottom':[]}}

    signals['rsi']['bull'], signals['rsi']['bear'] = detect_divergence_price_vs_indicator(close, df['rsi'], lows, highs)
    signals['cci']['bull'], signals['cci']['bear'] = detect_divergence_price_vs_indicator(close, df['cci'], lows, highs)
    signals['mfi']['bull'], signals['mfi']['bear'] = detect_divergence_price_vs_indicator(close, df['mfi'], lows, highs)
    signals['kd']['bull'], signals['kd']['bear'] = detect_kd_divergence(close, df['k'])
    signals['bollinger']['top'], signals['bollinger']['bottom'] = detect_bollinger_reversal(df['pctb'])

    # 合并索引到 signal_table
    idx_to_signals={}
    def add_signal(idx,name,side):
        if idx not in idx_to_signals: idx_to_signals[idx]=[]
        idx_to_signals[idx].append(f"{name}:{side}")

    for name in ['rsi','cci','mfi','kd']:
        for i in signals[name]['bull']: add_signal(int(i),name,'bull')
        for i in signals[name]['bear']: add_signal(int(i),name,'bear')

    for i in signals['bollinger']['top']: add_signal(int(i),'bollinger','top')
    for i in signals['bollinger']['bottom']: add_signal(int(i),'bollinger','bottom')

    signal_table=[]
    for idx,items in sorted(idx_to_signals.items()):
        signal_table.append({'index':int(idx),'date':df.loc[idx,'date'],'close':float(df.loc[idx,'close']),'signals':items})

    strong=[row for row in signal_table if len({s.split(':')[0] for s in row['signals']})>=2]

    return df, signals, signal_table, strong

# --------------------------
# 5) 绘图：主图 + hover
# --------------------------
def plot_main_only(df, signals, signal_table, strong):
    df=df.copy()
    df['date']=pd.to_datetime(df['date'])
    fig,ax=plt.subplots(figsize=(16,8))
    line_price,=ax.plot(df['date'],df['close'],label='Close',lw=1.2)
    line_price._df_index=df.index.to_numpy()

    def draw_scatter(inds,color,marker,label=None,size=80):
        if len(inds)==0: return None
        sc=ax.scatter(df['date'].iloc[inds],df['close'].iloc[inds],color=color,marker=marker,
                      s=size,label=label,zorder=5,edgecolors='black',linewidths=0.4)
        sc._df_index=df.index.to_numpy()[inds]
        return sc

    scatters=[]
    mapping={'rsi':('green','^'),'cci':('purple','h'),'mfi':('teal','D'),'kd':('magenta','v'),'bollinger':('black','X')}

    for name in ['rsi','cci','mfi','kd']:
        col,mark=mapping[name]
        b=np.array(signals[name]['bull'],dtype=int) if len(signals[name]['bull'])>0 else np.array([],dtype=int)
        r=np.array(signals[name]['bear'],dtype=int) if len(signals[name]['bear'])>0 else np.array([],dtype=int)
        scatters.append(draw_scatter(b,col,mark,label=f"{name} bull"))
        scatters.append(draw_scatter(r,col,mark,label=f"{name} bear"))

    btop=np.array(signals['bollinger']['top'],dtype=int) if len(signals['bollinger']['top'])>0 else np.array([],dtype=int)
    bbot=np.array(signals['bollinger']['bottom'],dtype=int) if len(signals['bollinger']['bottom'])>0 else np.array([],dtype=int)
    scatters.append(draw_scatter(btop,'black','X','BB top'))
    scatters.append(draw_scatter(bbot,'black','1','BB bottom'))

    strong_idx=np.array([r['index'] for r in strong],dtype=int) if len(strong)>0 else np.array([],dtype=int)
    strong_idx_bear = [r['index'] for r in strong if any('bear' in s for s in r['signals'])]
    strong_sc=None
    if len(strong_idx)>0:
        strong_sc=ax.scatter(df['date'].iloc[strong_idx],df['close'].iloc[strong_idx],
                             color='gold',s=220,marker='*',edgecolors='black',label='STRONG bull',zorder=6)
        strong_sc._df_index=df.index.to_numpy()[strong_idx]
    if len(strong_idx_bear) > 0:
        sc_bear = ax.scatter(df['date'].iloc[strong_idx_bear], df['close'].iloc[strong_idx_bear],
                             color='red', s=220, marker='*', edgecolors='black', label='STRONG bear', zorder=6)
        sc_bear._df_index = df.index.to_numpy()[strong_idx_bear]

    ax.legend(loc='upper left',fontsize=8)
    artists=[s for s in scatters if s is not None]
    if strong_sc is not None: artists.append(strong_sc)
    artists.append(line_price)

    cursor=mplcursors.cursor(artists,hover=True)
    @cursor.connect("add")
    def on_add(sel):
        art=sel.artist
        if not hasattr(art,'_df_index'):
            idx=sel.index
            if idx<len(df):
                row=df.iloc[idx]
                sel.annotation.set(text=f"{row['date'].strftime('%Y-%m-%d')}\nClose: {row['close']:.2f}",fontsize=9)
            return
        true_idx=int(art._df_index[sel.index])
        row=df.loc[true_idx]
        sigs=[]
        for nm in ['rsi','cci','mfi','kd']:
            if true_idx in signals[nm]['bull']: sigs.append(f"{nm}:bull")
            if true_idx in signals[nm]['bear']: sigs.append(f"{nm}:bear")
        if true_idx in signals['bollinger']['top']: sigs.append('bollinger:top')
        if true_idx in signals['bollinger']['bottom']: sigs.append('bollinger:bottom')
        names_set={s.split(':')[0] for s in sigs}
        stars='' if len(names_set)<2 else '*'*len(names_set)
        strong_flag='  STRONG' if true_idx in strong_idx else ''
        txt=(f"{row['date'].strftime('%Y-%m-%d')}\n"
             f"Close: {row['close']:.2f}\n"
             f"Signals: {', '.join(sigs)}{stars}{strong_flag}\n\n"
             f"RSI={row['rsi']:.2f}  %B={row['pctb']:.2f}\n"
             f"K={row['k']:.2f} / D={row['d']:.2f}\n"
             f"CCI={row['cci']:.2f}  MFI={row['mfi']:.2f}")
        sel.annotation.set(text=txt,fontsize=9)

    ax.set_title("Main Chart — Multi-Indicator Signals (hover for details)")
    ax.grid(True)
    plt.tight_layout()
    plt.show()


# --------------------------
# 6) 使用示例（随机数据 demo） — 替换为你的 df 即可
# --------------------------
if __name__ == "__main__":
    np.random.seed(42)
    N = 300
    rng = pd.date_range("2024-01-01", periods=N, freq='B')
    open_p = 100 + np.cumsum(np.random.randn(N) * 0.5)
    # small move to close
    close_p = open_p + np.random.randn(N) * 0.6
    volume = (np.abs(np.random.randn(N)) * 1000).astype(int) + 100

    df_demo = pd.DataFrame({
        "date": rng,
        "open": open_p,
        "close": close_p,
        "volume": volume
    })

    # df = pd.read_csv(glob.glob("../output/price/2025/qqq/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/iren/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2024/iren/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2023/iren/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2022/iren/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/amd/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2022/amd/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/nbis/part-00000-*-c000.csv")[0])
    df = pd.read_csv(glob.glob("../output/price/2025/cifr/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/wulf/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/onds/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2024/onds/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/oklo/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/avgo/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2024/avgo/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2023/avgo/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/tsla/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/nvda/part-00000-*-c000.csv")[0])


    df_calc, signals, table, strong = multi_indicator_signals(df)
    print("Signal table (first 20):")
    for r in table[:20]:
        print(r)
    print("\nStrong signals:")
    for s in strong:
        print(s)

    plot_main_only(df_calc, signals, table, strong)

