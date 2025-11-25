import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplcursors
import glob

# -------------------- 指标函数 --------------------
def compute_rsi(close, period=14):
    delta = close.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    ma_up = up.ewm(alpha=1/period, adjust=False).mean()
    ma_down = down.ewm(alpha=1/period, adjust=False).mean()
    rs = ma_up / (ma_down.replace(0, np.nan))
    rsi = 100 - 100/(1+rs)
    return rsi.fillna(50)

def compute_macd(close, short=12, long=26, signal=9):
    ema_short = close.ewm(span=short, adjust=False).mean()
    ema_long = close.ewm(span=long, adjust=False).mean()
    diff = ema_short - ema_long
    dea = diff.ewm(span=signal, adjust=False).mean()
    hist = (diff - dea) * 2
    return diff, dea, hist

def compute_stochastic(high_like, low_like, close, k_period=14, d_period=3):
    # We only have close; emulate high/low via rolling max/min on close
    highest = high_like.rolling(k_period, min_periods=1).max()
    lowest = low_like.rolling(k_period, min_periods=1).min()
    k = 100 * (close - lowest) / (highest - lowest + 1e-9)
    d = k.rolling(d_period, min_periods=1).mean()
    return k.fillna(50), d.fillna(50)

def compute_cci(high_like, low_like, close, n=20):
    # typical price = (high+low+close)/3, emulate high/low using rolling extrema if not available
    tp = (high_like + low_like + close) / 3.0
    ma = tp.rolling(n, min_periods=1).mean()
    md = tp.rolling(n, min_periods=1).apply(lambda x: np.mean(np.abs(x - np.mean(x))), raw=True)
    cci = (tp - ma) / (0.015 * (md + 1e-9))
    return cci.fillna(0)

def compute_mfi(close, volume, n=14):
    # MFI needs typical price and volume. If volume missing, return NaN series
    if volume.isna().all():
        return pd.Series(np.nan, index=close.index)
    high_like = close.rolling(n, min_periods=1).max()
    low_like = close.rolling(n, min_periods=1).min()
    tp = (high_like + low_like + close) / 3.0
    raw = tp * volume
    positive = []
    negative = []
    for i in range(1, len(tp)):
        if tp.iloc[i] > tp.iloc[i-1]:
            positive.append(raw.iloc[i])
            negative.append(0.0)
        else:
            positive.append(0.0)
            negative.append(raw.iloc[i])
    # pad first element
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

# -------------------- 无未来的 swing high/low（实盘可用） --------------------
def find_swings_no_lookahead(series):
    """
    定义：i 为 low 当且仅当 close[i] < close[i-1] and close[i] < close[i-2]
            i 为 high 当且仅当 close[i] > close[i-1] and close[i] > close[i-2]
    返回 index arrays (lows, highs)
    """
    lows = []
    highs = []
    arr = series.values
    for i in range(2, len(arr)):
        if arr[i] < arr[i-1] and arr[i] < arr[i-2]:
            lows.append(i)
        if arr[i] > arr[i-1] and arr[i] > arr[i-2]:
            highs.append(i)
    return np.array(lows, dtype=int), np.array(highs, dtype=int)

# -------------------- 背离检测（通用） --------------------
def detect_divergence_price_vs_indicator(price, indicator, swing_lows=None, swing_highs=None):
    """
    price, indicator: pd.Series aligned
    swing_lows/highs: optional precomputed arrays; if None, compute from price
    返回 (bull_indices, bear_indices) - indices in the series (int list)
    bull: price makes lower low (p1>p2) while indicator makes higher low (ind1<ind2) => bullish divergence
    bear: price makes higher high while indicator makes lower high => bearish divergence
    """
    if swing_lows is None or swing_highs is None:
        lows, highs = find_swings_no_lookahead(price)
    else:
        lows, highs = swing_lows, swing_highs

    bullish = []
    bearish = []

    # bullish: compare consecutive lows
    for i in range(1, len(lows)):
        p1, p2 = lows[i-1], lows[i]
        if price.iloc[p2] < price.iloc[p1] and indicator.iloc[p2] > indicator.iloc[p1]:
            bullish.append(p2)

    # bearish: consecutive highs
    for i in range(1, len(highs)):
        p1, p2 = highs[i-1], highs[i]
        if price.iloc[p2] > price.iloc[p1] and indicator.iloc[p2] < indicator.iloc[p1]:
            bearish.append(p2)

    return np.array(bullish, dtype=int), np.array(bearish, dtype=int)

# -------------------- Bollinger %B 反转探测（无未来） --------------------
def detect_bollinger_reversal(pctb):
    """
    简单规则（无未来）：
      - Top signal: 当 pctb 前一日 >1, 当日 <=1 (从上轨回落)
      - Bottom signal: 当 pctb 前一日 <0, 当日 >=0 (从下轨反弹)
    返回 (tops, bottoms)
    """
    tops = []
    bottoms = []
    p = pctb.values
    for i in range(1, len(p)):
        if p[i-1] > 1 and p[i] <= 1:
            tops.append(i)
        if p[i-1] < 0 and p[i] >= 0:
            bottoms.append(i)
    return np.array(tops, dtype=int), np.array(bottoms, dtype=int)

# -------------------- 主流程：整合指标 + 检测 --------------------
def multi_indicator_signals(df):
    df = df.copy().reset_index(drop=True)
    df['date'] = pd.to_datetime(df['date'])
    close = df['close'].astype(float)

    df['rsi'] = compute_rsi(close)
    df['diff'], df['dea'], df['macd_hist'] = compute_macd(close)
    df['k'], df['d'] = compute_stochastic(df['high'], df['low'], close)
    df['cci'] = compute_cci(df['high'], df['low'], close)
    df['mfi'] = compute_mfi(close, df['volume'] if 'volume' in df.columns else pd.Series(np.nan, index=df.index))
    df['pctb'], df['bb_upper'], df['bb_lower'] = compute_bollinger_pctb(close)

    # swings based on price (no lookahead)
    lows, highs = find_swings_no_lookahead(close)

    signals = { 'rsi': {'bull':[], 'bear':[]},
                'macd': {'bull':[], 'bear':[]},
                'stochastic': {'bull':[], 'bear':[]},
                'cci': {'bull':[], 'bear':[]},
                'mfi': {'bull':[], 'bear':[]},
                'bollinger': {'top':[], 'bottom':[]}
              }

    # detect for each
    r_bull, r_bear = detect_divergence_price_vs_indicator(close, df['rsi'], swing_lows=lows, swing_highs=highs)
    signals['rsi']['bull'] = list(r_bull); signals['rsi']['bear'] = list(r_bear)

    m_bull, m_bear = detect_divergence_price_vs_indicator(close, df['diff'], swing_lows=lows, swing_highs=highs)
    signals['macd']['bull'] = list(m_bull); signals['macd']['bear'] = list(m_bear)

    s_bull, s_bear = detect_divergence_price_vs_indicator(close, df['k'], swing_lows=lows, swing_highs=highs)
    signals['stochastic']['bull'] = list(s_bull); signals['stochastic']['bear'] = list(s_bear)

    c_bull, c_bear = detect_divergence_price_vs_indicator(close, df['cci'], swing_lows=lows, swing_highs=highs)
    signals['cci']['bull'] = list(c_bull); signals['cci']['bear'] = list(c_bear)

    if not df['mfi'].isna().all():
        f_bull, f_bear = detect_divergence_price_vs_indicator(close, df['mfi'], swing_lows=lows, swing_highs=highs)
        signals['mfi']['bull'] = list(f_bull); signals['mfi']['bear'] = list(f_bear)
    else:
        signals['mfi']['bull'] = []; signals['mfi']['bear'] = []

    # bollinger reversals
    tops, bottoms = detect_bollinger_reversal(df['pctb'])
    signals['bollinger']['top'] = list(tops); signals['bollinger']['bottom'] = list(bottoms)

    # 合并: 为每个 index 统计哪些指标给出了信号
    idx_to_signals = {}
    def add_signal(idx, name, side):
        if idx not in idx_to_signals:
            idx_to_signals[idx] = []
        idx_to_signals[idx].append(f"{name}:{side}")

    for name in ['rsi','macd','stochastic','cci','mfi']:
        for i in signals[name]['bull']:
            add_signal(i, name, 'bull')
        for i in signals[name]['bear']:
            add_signal(i, name, 'bear')

    for i in signals['bollinger']['top']:
        add_signal(i, 'bollinger', 'top')
    for i in signals['bollinger']['bottom']:
        add_signal(i, 'bollinger', 'bottom')

    # generate lists
    signal_table = []
    for idx, items in sorted(idx_to_signals.items()):
        signal_table.append({'index': int(idx), 'date': df.loc[idx,'date'], 'close': float(df.loc[idx,'close']), 'signals': items})

    # strong signals: 当一个 index 有至少两个不同指标（或 bollinger+另一个）发出信号（方向可混合）
    strong = [row for row in signal_table if len({s.split(':')[0] for s in row['signals']}) >= 2]

    return df, signals, signal_table, strong

# -------------------- 绘图（matplotlib + mplcursors） --------------------
def plot_signals(df, signals, signal_table, strong):
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])

    fig, axes = plt.subplots(6, 1, figsize=(14, 18), sharex=True,
                             gridspec_kw={'height_ratios':[2,1,1,1,1,1]})

    ax_price = axes[0]
    ax_rsi = axes[1]
    ax_macd = axes[2]
    ax_sto = axes[3]
    ax_cci = axes[4]
    ax_mfi = axes[5]

    # price
    line_price, = ax_price.plot(df['date'], df['close'], label='Close', linewidth=1)
    line_price._df_index = df.index.to_numpy()

    # plot indicators
    ax_rsi.plot(df['date'], df['rsi'], label='RSI'); ax_rsi.axhline(70, color='gray', ls='--'); ax_rsi.axhline(30, color='gray', ls='--')
    line_rsi, = ax_rsi.plot([], [])  # placeholder
    line_rsi._df_index = df.index.to_numpy()

    ax_macd.plot(df['date'], df['diff'], label='DIFF'); ax_macd.plot(df['date'], df['dea'], label='DEA')
    ax_macd.bar(df['date'], df['macd_hist'], width=1, label='HIST', color=[ 'red' if x<0 else 'green' for x in df['macd_hist'] ])
    line_macd, = ax_macd.plot([], [])
    line_macd._df_index = df.index.to_numpy()

    ax_sto.plot(df['date'], df['k'], label='%K'); ax_sto.plot(df['date'], df['d'], label='%D'); ax_sto.axhline(80, color='gray', ls='--'); ax_sto.axhline(20, color='gray', ls='--')
    line_sto, = ax_sto.plot([], [])
    line_sto._df_index = df.index.to_numpy()

    ax_cci.plot(df['date'], df['cci'], label='CCI'); ax_cci.axhline(100, color='gray', ls='--'); ax_cci.axhline(-100, color='gray', ls='--')
    line_cci, = ax_cci.plot([], [])
    line_cci._df_index = df.index.to_numpy()

    ax_mfi.plot(df['date'], df['mfi'], label='MFI')
    line_mfi, = ax_mfi.plot([], [])
    line_mfi._df_index = df.index.to_numpy()

    # plot individual indicator signals as scatter on price and on respective subplots
    artist_list = [line_price, line_rsi, line_macd, line_sto, line_cci, line_mfi]
    idx_map = {}  # map artist -> df_index_array

    # helper to draw scatters and attach _df_index
    def draw_scatter(ax, inds, yvals, color, marker, label):
        if len(inds)==0:
            return None
        dates = df['date'].iloc[inds].values
        ys = yvals[inds]
        sc = ax.scatter(dates, ys, color=color, s=60, marker=marker, label=label, zorder=5)
        sc._df_index = df.index.to_numpy()[inds]
        return sc

    # draw per-indicator signals
    scatters = []
    # RSI
    scatters.append(draw_scatter(ax_price, np.array(signals['rsi']['bull']), df['close'].values, 'green', '^', 'RSI Bull'))
    scatters.append(draw_scatter(ax_price, np.array(signals['rsi']['bear']), df['close'].values, 'red', 'v', 'RSI Bear'))
    scatters.append(draw_scatter(ax_rsi, np.array(signals['rsi']['bull']), df['rsi'].values, 'green', '^', None))
    scatters.append(draw_scatter(ax_rsi, np.array(signals['rsi']['bear']), df['rsi'].values, 'red', 'v', None))

    # MACD
    scatters.append(draw_scatter(ax_price, np.array(signals['macd']['bull']), df['close'].values, 'lime', 'P', 'MACD Bull'))
    scatters.append(draw_scatter(ax_price, np.array(signals['macd']['bear']), df['close'].values, 'orange', 'p', 'MACD Bear'))
    scatters.append(draw_scatter(ax_macd, np.array(signals['macd']['bull']), df['diff'].values, 'lime', 'P', None))
    scatters.append(draw_scatter(ax_macd, np.array(signals['macd']['bear']), df['diff'].values, 'orange', 'p', None))

    # Stochastic
    scatters.append(draw_scatter(ax_price, np.array(signals['stochastic']['bull']), df['close'].values, 'darkgreen', '>', 'STO Bull'))
    scatters.append(draw_scatter(ax_price, np.array(signals['stochastic']['bear']), df['close'].values, 'darkred', '<', 'STO Bear'))
    scatters.append(draw_scatter(ax_sto, np.array(signals['stochastic']['bull']), df['k'].values, 'darkgreen', '>', None))
    scatters.append(draw_scatter(ax_sto, np.array(signals['stochastic']['bear']), df['k'].values, 'darkred', '<', None))

    # CCI
    scatters.append(draw_scatter(ax_price, np.array(signals['cci']['bull']), df['close'].values, 'teal', 'h', 'CCI Bull'))
    scatters.append(draw_scatter(ax_price, np.array(signals['cci']['bear']), df['close'].values, 'maroon', 'H', 'CCI Bear'))
    scatters.append(draw_scatter(ax_cci, np.array(signals['cci']['bull']), df['cci'].values, 'teal', 'h', None))
    scatters.append(draw_scatter(ax_cci, np.array(signals['cci']['bear']), df['cci'].values, 'maroon', 'H', None))

    # MFI
    if not df['mfi'].isna().all():
        scatters.append(draw_scatter(ax_price, np.array(signals['mfi']['bull']), df['close'].values, 'blue', 'D', 'MFI Bull'))
        scatters.append(draw_scatter(ax_price, np.array(signals['mfi']['bear']), df['close'].values, 'purple', 'd', 'MFI Bear'))
        scatters.append(draw_scatter(ax_mfi, np.array(signals['mfi']['bull']), df['mfi'].values, 'blue', 'D', None))
        scatters.append(draw_scatter(ax_mfi, np.array(signals['mfi']['bear']), df['mfi'].values, 'purple', 'd', None))

    # Bollinger tops/bottoms
    scatters.append(draw_scatter(ax_price, np.array(signals['bollinger']['top']), df['close'].values, 'black', 'X', 'BB Top'))
    scatters.append(draw_scatter(ax_price, np.array(signals['bollinger']['bottom']), df['close'].values, 'black', '1', 'BB Bottom'))
    scatters.append(draw_scatter(ax_rsi, np.array(signals['bollinger']['top']), df['rsi'].values, 'black', 'X', None))
    scatters.append(draw_scatter(ax_rsi, np.array(signals['bollinger']['bottom']), df['rsi'].values, 'black', '1', None))

    # strong signals - draw larger yellow star on price
    strong_indices = np.array([row['index'] for row in signal_table if len({s.split(':')[0] for s in row['signals']})>=2], dtype=int)
    strong_sc = None
    if len(strong_indices)>0:
        strong_sc = ax_price.scatter(df['date'].iloc[strong_indices], df['close'].iloc[strong_indices],
                                     color='gold', s=140, marker='*', edgecolors='black', label='STRONG')
        strong_sc._df_index = df.index.to_numpy()[strong_indices]

    ax_price.legend(loc='upper left', fontsize=8)
    ax_rsi.legend(loc='upper left', fontsize=8)
    ax_macd.legend(loc='upper left', fontsize=8)
    ax_sto.legend(loc='upper left', fontsize=8)
    ax_cci.legend(loc='upper left', fontsize=8)
    ax_mfi.legend(loc='upper left', fontsize=8)

    # ---- Hover tooltip using mplcursors, binding exact index to artist ----
    artists_for_cursor = [line_price]
    # include all scatters that are not None
    for sc in scatters:
        if sc is not None:
            artists_for_cursor.append(sc)
    if strong_sc is not None:
        artists_for_cursor.append(strong_sc)
    # include empty placeholder lines for indicators to allow cursor on their lines
    artists_for_cursor += [line_rsi, line_macd, line_sto, line_cci, line_mfi]

    cursor = mplcursors.cursor(artists_for_cursor, hover=True)

    @cursor.connect("add")
    def on_add(sel):
        art = sel.artist
        # some artists (like bars) might not have _df_index; handle gracefully
        if hasattr(art, "_df_index"):
            true_idx = int(art._df_index[sel.index])
            row = df.loc[true_idx]
            # collect any signals at this idx
            sigs = []
            for s in ['rsi','macd','stochastic','cci','mfi']:
                if true_idx in signals[s]['bull']:
                    sigs.append(f"{s}:bull")
                if true_idx in signals[s]['bear']:
                    sigs.append(f"{s}:bear")
            if true_idx in signals['bollinger']['top']:
                sigs.append('bollinger:top')
            if true_idx in signals['bollinger']['bottom']:
                sigs.append('bollinger:bottom')
            # strong?
            strong_flag = 'STRONG' if true_idx in (strong_indices if len(strong_indices)>0 else []) else ''
            sel.annotation.set(
                text=f"{row['date'].strftime('%Y-%m-%d')}\nClose:{row['close']:.2f}\nSignals:{','.join(sigs)}\n{strong_flag}",
                fontsize=9
            )
        else:
            # fallback: try to use sel.index as df index
            idx = sel.index
            if idx < len(df):
                row = df.iloc[idx]
                sel.annotation.set(text=f"{row['date'].strftime('%Y-%m-%d')}\nClose:{row['close']:.2f}", fontsize=9)
            else:
                sel.annotation.set(text="")

    plt.tight_layout()
    plt.show()

# -------------------- 运行示例 --------------------
if __name__ == "__main__":
    # df = pd.read_csv(glob.glob("../output/price/2025/qqq/part-00000-*-c000.csv")[0])
    df = pd.read_csv(glob.glob("../output/price/2025/2025-11-24/iren/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2024/iren/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2023/iren/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2022/iren/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/amd/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/nbis/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/cifr/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/wulf/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/onds/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2024/onds/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/oklo/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2025/avgo/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2024/avgo/part-00000-*-c000.csv")[0])
    # df = pd.read_csv(glob.glob("../output/price/2023/avgo/part-00000-*-c000.csv")[0])

    df, signals, table, strong = multi_indicator_signals(df)
    print("Detected signal summary (first 20):")
    for r in table[:20]:
        print(r['index'], r['date'].strftime('%Y-%m-%d'), r['close'], r['signals'])
    print("\nStrong signals (>=2 different indicators):")
    for r in strong:
        print(r['index'], r['date'].strftime('%Y-%m-%d'), r['close'], r['signals'])

    plot_signals(df, signals, table, strong)
