import glob
import mplcursors
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date, timedelta

def plot_price_rsi(df):
    df["date"] = pd.to_datetime(df["date"])

    # 创建主图和 RSI 图
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), sharex=True)

    # 主图：绘制收盘价
    ax1.plot(df["date"], df["close"], label="Close Price", lw=1.2, color='blue')
    ax1.set_title("Price Chart")
    ax1.set_ylabel("Price")
    ax1.grid(True)

    # 绘制 RSI 图
    ax2.plot(df["date"], df["rsi"], label="RSI", lw=1.2, color='purple')

    # 添加水平线，标示超买区（70）和超卖区（30）
    ax2.axhline(70, color='red', linestyle="--", label="Overbought (70)")
    ax2.axhline(30, color='green', linestyle="--", label="Oversold (30)")

    ax2.set_title("RSI Chart")
    ax2.set_ylabel("RSI")
    ax2.set_ylim(0, 100)
    ax2.grid(True)
    ax2.legend(loc='upper left')

    # 调整图表布局
    plt.tight_layout()

    # 显示图表
    plt.show()

# 示例数据：包括日期、开盘、最高、最低、收盘、交易量以及MACD相关数据
def plot_price_macd(df):
    df['date'] = pd.to_datetime(df['date'])

    # 计算买入/卖出信号
    df['buy_signal'] = (df['macd'] > df['macd_signal']) & (df['macd'].shift(1) < df['macd_signal'].shift(1))
    df['sell_signal'] = (df['macd'] < df['macd_signal']) & (df['macd'].shift(1) > df['macd_signal'].shift(1))

    # 设置图形大小
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), sharex=True)

    # 绘制主图（价格）
    ax1.plot(df['date'], df['close'], label='Close Price', color='b', linewidth=1.2)
    ax1.set_title('Stock Price and MACD', fontsize=14)
    ax1.set_ylabel('Price', fontsize=12)
    ax1.grid(True)
    ax1.legend(loc='upper left')

    # 绘制 MACD 图
    ax2.plot(df['date'], df['macd'], label='MACD', color='r', linewidth=1.2)
    ax2.plot(df['date'], df['macd_signal'], label='MACD Signal', color='g', linewidth=1.2)
    ax2.bar(df['date'], df['macd_hist'], label='MACD Histogram', color='gray', alpha=0.3)

    # 绘制买入和卖出信号
    buy_points = ax2.scatter(df['date'][df['buy_signal']], df['macd'][df['buy_signal']], marker='^', color='g',
                             label='Buy Signal', s=100)
    sell_points = ax2.scatter(df['date'][df['sell_signal']], df['macd'][df['sell_signal']], marker='v', color='r',
                              label='Sell Signal', s=100)

    # 使用mplcursors来实现鼠标悬停显示值
    cursor = mplcursors.cursor([buy_points, sell_points], hover=True)

    # 创建一个外部函数来显示信号的详细信息
    def on_hover(sel):
        # 获取被悬停的点
        ind = sel.index
        row = df.iloc[ind]  # 获取行数据
        signal_type = 'Buy' if row['buy_signal'] else 'Sell'  # 判断信号类型

        # 创建正确格式的显示文本
        text = (
            f"Date: {row['date'].strftime('%Y-%m-%d')}\n"  # 格式化日期
            f"Signal: {signal_type}\n"
            f"MACD: {row['macd']:.2f}\n"
            f"MACD Signal: {row['macd_signal']:.2f}\n"
            f"MACD Histogram: {row['macd_hist']:.2f}"
        )
        sel.annotation.set(text=text, fontsize=9)

    # 连接悬停事件
    cursor.connect("add", on_hover)

    # 设置图形标题和标签
    ax2.set_title('MACD and Signal with Buy/Sell Signals', fontsize=14)
    ax2.set_ylabel('MACD', fontsize=12)
    ax2.grid(True)
    ax2.legend(loc='upper left')

    # 自动调整布局
    plt.tight_layout()

    # 显示图表
    plt.show()


from pyecharts.charts import Line, Bar, Grid
from pyecharts import options as opts
import pandas as pd

def plot_price_turning_points(df, html_file="turning_points_macd.html"):
    df["date"] = pd.to_datetime(df["date"])
    df["date_str"] = df["date"].dt.strftime("%Y-%m-%d")

    # -------- 拐点检测：看涨 / 看跌 --------
    bullish = []
    bearish = []

    for i in range(len(df)):
        if i == 0 or i == len(df) - 1:
            bullish.append(None)
            bearish.append(None)
            continue

        # 底部拐点（看涨）
        if df["close"].iloc[i-1] > df["close"].iloc[i] < df["close"].iloc[i+1]:
            bullish.append(df["close"].iloc[i])
            bearish.append(None)
        # 顶部拐点（看跌）
        elif df["close"].iloc[i-1] < df["close"].iloc[i] > df["close"].iloc[i+1]:
            bearish.append(df["close"].iloc[i])
            bullish.append(None)
        else:
            bullish.append(None)
            bearish.append(None)

    # -------- 价格曲线 --------
    price_line = (
        Line()
        .add_xaxis(df["date_str"].tolist())
        .add_yaxis("Close Price", df["close"].tolist(), linestyle_opts=opts.LineStyleOpts(width=1.5))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Price + Turning Point Signals"),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")]
        )
    )

    # -------- 拐点标记覆盖在价格图 --------
    # price_line.add_yaxis(
    #     "Bullish ▲",
    #     bullish,
    #     symbol="triangle",
    #     symbol_size=13,
    #     itemstyle_opts=opts.ItemStyleOpts(color="green"),
    #     label_opts=opts.LabelOpts(is_show=False)
    # )
    #
    # price_line.add_yaxis(
    #     "Bearish ▼",
    #     bearish,
    #     symbol="triangle-down",
    #     symbol_size=13,
    #     itemstyle_opts=opts.ItemStyleOpts(color="red"),
    #     label_opts=opts.LabelOpts(is_show=False)
    # )

    # -------- MACD 主图 --------
    macd_line = (
        Line()
        .add_xaxis(df['date_str'].tolist())
        .add_yaxis("MACD", df['macd'].tolist(), linestyle_opts=opts.LineStyleOpts(width=1.5, color="red"))
        .add_yaxis("MACD Signal", df['macd_signal'].tolist(), linestyle_opts=opts.LineStyleOpts(width=1.5, color="green"))
    )
    macd_bar = (
        Bar()
        .add_xaxis(df['date_str'].tolist())
        .add_yaxis("MACD Histogram", df['macd_hist'].tolist(), label_opts=opts.LabelOpts(is_show=False))
    )
    macd_combo = macd_line.overlap(macd_bar).set_global_opts(
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        legend_opts=opts.LegendOpts(pos_left="left")
    )

    # -------- 上下布局 --------
    grid = Grid(init_opts=opts.InitOpts(width="1400px", height="860px"))
    grid.add(price_line, grid_opts=opts.GridOpts(pos_bottom="55%"))
    grid.add(macd_combo, grid_opts=opts.GridOpts(pos_top="50%"))
    grid.render(html_file)
    print("HTML 图表已生成：", html_file)



# 示例数据：包括日期、开盘、最高、最低、收盘、交易量以及MACD相关数据
def plot_price_mfi(df):
    # 确保 'date' 列为日期格式
    df['date'] = pd.to_datetime(df['date'])

    # ==========================
    # 检测 MFI 买卖信号
    # ==========================
    # 买入信号：MFI < 20 且 MFI 从低位上升
    df['buy_signal'] = (df['mfi'] < 20) & (df['mfi'].shift(1) < 20) & (df['mfi'] > df['mfi'].shift(1))

    # 卖出信号：MFI > 80 且 MFI 从高位下降
    df['sell_signal'] = (df['mfi'] > 80) & (df['mfi'].shift(1) > 80) & (df['mfi'] < df['mfi'].shift(1))

    # ==========================
    # 绘制图表
    # ==========================
    # 设置图形大小
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), sharex=True)

    # 绘制主图（价格）
    ax1.plot(df['date'], df['close'], label='Close Price', color='b', linewidth=1.2)
    ax1.set_title('Stock Price with MFI Buy/Sell Signals', fontsize=14)
    ax1.set_ylabel('Price', fontsize=12)
    ax1.grid(True)
    ax1.legend(loc='upper left')

    # 绘制 MFI 图
    ax2.plot(df['date'], df['mfi'], label='MFI', color='orange', linewidth=1.2)

    # 绘制买入和卖出信号
    ax2.scatter(df['date'][df['buy_signal']], df['mfi'][df['buy_signal']], marker='^', color='g', label='Buy Signal',
                s=100)
    ax2.scatter(df['date'][df['sell_signal']], df['mfi'][df['sell_signal']], marker='v', color='r', label='Sell Signal',
                s=100)

    ax2.set_title('MFI and Buy/Sell Signals', fontsize=14)
    ax2.set_ylabel('MFI', fontsize=12)
    ax2.axhline(20, color='g', linestyle='--', label='MFI Buy Threshold (20)')
    ax2.axhline(80, color='r', linestyle='--', label='MFI Sell Threshold (80)')
    ax2.grid(True)
    ax2.legend(loc='upper left')

    # 自动调整布局
    plt.tight_layout()

    # 显示图表
    plt.show()


def plot_price_kd(df):
    df['date'] = pd.to_datetime(df['date'])

    # 计算买入/卖出信号
    df['buy_signal'] = (df['fast_k'] > df['fast_d']) & (df['fast_k'].shift(1) < df['fast_d'].shift(1)) & (
                df['fast_k'] < 20)
    df['sell_signal'] = (df['fast_k'] < df['fast_d']) & (df['fast_k'].shift(1) > df['fast_d'].shift(1)) & (
                df['fast_k'] > 80)

    # 设置图形大小
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), sharex=True)

    # 绘制主图（价格）
    # 假设你有价格数据（例如 'close'），此处模拟绘制价格
    ax1.plot(df['date'], df['close'], label='Close Price', color='blue', linewidth=1.2)  # 模拟的收盘价
    ax1.set_title('Stock Price and KD Indicator', fontsize=14)
    ax1.set_ylabel('Price', fontsize=12)
    ax1.grid(True)
    ax1.legend(loc='upper left')

    # 绘制 KD 图（fast_k 和 fast_d）
    ax2.plot(df['date'], df['fast_k'], label='fast_k', color='orange', linewidth=1.2)
    ax2.plot(df['date'], df['fast_d'], label='fast_d', color='green', linewidth=1.2)
    ax2.axhline(80, color='r', linestyle='--', label='Overbought (80)')
    ax2.axhline(20, color='g', linestyle='--', label='Oversold (20)')

    # 绘制买入和卖出信号
    ax2.scatter(df['date'][df['buy_signal']], df['fast_k'][df['buy_signal']], marker='^', color='g', label='Buy Signal',
                s=100)
    ax2.scatter(df['date'][df['sell_signal']], df['fast_k'][df['sell_signal']], marker='v', color='r',
                label='Sell Signal', s=100)

    ax2.set_title('KD Indicator with Buy/Sell Signals', fontsize=14)
    ax2.set_ylabel('KD Value', fontsize=12)
    ax2.grid(True)
    ax2.legend(loc='upper left')

    # 自动调整布局
    plt.tight_layout()

    # 显示图表
    plt.show()


def plot_price_cci(df):
    # 检测买入和卖出信号
    # 买入信号：CCI从下方穿越-100
    # 卖出信号：CCI从上方穿越+100
    df['buy_signal'] = (df['cci'] < -100) & (df['cci'].shift(1) >= -100)
    df['sell_signal'] = (df['cci'] > 100) & (df['cci'].shift(1) <= 100)

    # 设置图形大小
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), sharex=True)

    # 绘制主图（价格）
    ax1.plot(df['date'], df['close'], label='Close Price', color='blue', linewidth=1.2)
    ax1.set_title('Stock Price and CCI Indicator', fontsize=14)
    ax1.set_ylabel('Price', fontsize=12)
    ax1.grid(True)
    ax1.legend(loc='upper left')

    # 绘制 CCI 图
    ax2.plot(df['date'], df['cci'], label='CCI', color='orange', linewidth=1.2)
    ax2.axhline(100, color='r', linestyle='--', label='Overbought (100)')
    ax2.axhline(-100, color='g', linestyle='--', label='Oversold (-100)')

    # 绘制买入和卖出信号
    ax2.scatter(df['date'][df['buy_signal']], df['cci'][df['buy_signal']], marker='^', color='g', label='Buy Signal',
                s=100)
    ax2.scatter(df['date'][df['sell_signal']], df['cci'][df['sell_signal']], marker='v', color='r', label='Sell Signal',
                s=100)

    ax2.set_title('CCI Indicator with Buy/Sell Signals', fontsize=14)
    ax2.set_ylabel('CCI Value', fontsize=12)
    ax2.grid(True)
    ax2.legend(loc='upper left')

    # 自动调整布局
    plt.tight_layout()

    # 显示图表
    plt.show()


# 示例调用
stock_anme = "amd"
end_date = "2025-11-27"
# 获取今日日期, 计算去年今日
# end_date = date.today()
df = pd.read_csv(glob.glob(f"output/rsi_union/2025/{end_date}/{stock_anme}/part-00000-*-c000.csv")[0])
plot_price_turning_points(df,f"macd_chart-{stock_anme}.html")
# plot_price_rsi(df)   # 底部是真底，一定买，一年中；顶部多且密
plot_price_kd(df)  # 看底非常好，是rsi的波动放大版；顶部多且密
# plot_price_macd(df)  # 看底非常好，比kd慢显现但是稳；


# plot_price_cci(df)   # amd买入卖出一样多，太密，作用不大
# plot_price_mfi(df) # amd完全不准，iren也不准
