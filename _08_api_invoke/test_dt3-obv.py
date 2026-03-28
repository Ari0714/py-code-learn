import glob

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ——————————————
# 输入数据 df: 必须包含 close、volume
# ——————————————
# 示例：读取本地 CSV
# df = pd.read_csv("data.csv")

from pyecharts.charts import Line
from pyecharts import options as opts

def calc_obv_signals(df, ma_period=9):
    df = df.copy()
    df["obv"] = 0

    # 逐条累加，无重绘
    for i in range(1, len(df)):
        if df.loc[i, "close"] > df.loc[i - 1, "close"]:
            df.loc[i, "obv"] = df.loc[i - 1, "obv"] + df.loc[i, "volume"]
        elif df.loc[i, "close"] < df.loc[i - 1, "close"]:
            df.loc[i, "obv"] = df.loc[i - 1, "obv"] - df.loc[i, "volume"]
        else:
            df.loc[i, "obv"] = df.loc[i - 1, "obv"]

    # OBV 均线
    df["obv_ma"] = df["obv"].rolling(ma_period).mean()

    # 买卖信号（无重绘）
    buy_signals = []
    sell_signals = []
    for i in range(1, len(df)):
        # 买入 = OBV 上穿均线
        if df.loc[i - 1, "obv"] < df.loc[i - 1, "obv_ma"] and df.loc[i, "obv"] > df.loc[i, "obv_ma"]:
            buy_signals.append((df.loc[i, "date"], df.loc[i, "obv"]))

        # 卖出 = OBV 下穿均线
        if df.loc[i - 1, "obv"] > df.loc[i - 1, "obv_ma"] and df.loc[i, "obv"] < df.loc[i, "obv_ma"]:
            sell_signals.append((df.loc[i, "date"], df.loc[i, "obv"]))

    return df, buy_signals, sell_signals

from pyecharts.charts import Line, Scatter
from pyecharts import options as opts

def plot_obv_signals(df):
    df["obv"] = df["obv"].astype(float)
    df["obv_ma"] = df["obv_ma"].astype(float)

    # === 生成买卖信号 ===
    buy_signals = []
    sell_signals = []

    for i in range(1, len(df)):
        prev_cross = df["obv"][i - 1] - df["obv_ma"][i - 1]
        now_cross = df["obv"][i] - df["obv_ma"][i]
        now_date = df["date"][i]
        now_obv = df["obv"][i]

        if prev_cross <= 0 and now_cross > 0:   # 上穿
            buy_signals.append((now_date, now_obv))
        if prev_cross >= 0 and now_cross < 0:   # 下穿
            sell_signals.append((now_date, now_obv))

    print("BUY signals:", buy_signals)
    print("SELL signals:", sell_signals)

    x = df["date"].tolist()
    obv = df["obv"].tolist()
    obv_ma = df["obv_ma"].tolist()

    chart = (
        Line()
        .add_xaxis(x)
        .add_yaxis("OBV", obv, is_smooth=True, linestyle_opts=opts.LineStyleOpts(width=2, color="orange"))
        .add_yaxis("OBV MA", obv_ma, is_smooth=True, linestyle_opts=opts.LineStyleOpts(width=2, color="blue"))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="OBV + Buy/Sell Signals"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
            legend_opts=opts.LegendOpts(pos_left="left"),
        )
    )

    # 买入 ▲ 绿色
    if buy_signals:
        chart = chart.overlap(
            Scatter()
            .add_xaxis([p[0] for p in buy_signals])
            .add_yaxis(
                "BUY",
                [p[1] for p in buy_signals],
                symbol="triangle",
                symbol_size=14,
                itemstyle_opts=opts.ItemStyleOpts(color="green"),
                label_opts=opts.LabelOpts(is_show=False),
            )
        )

    # 卖出 ▼ 红色
    if sell_signals:
        chart = chart.overlap(
            Scatter()
            .add_xaxis([p[0] for p in sell_signals])
            .add_yaxis(
                "SELL",
                [p[1] for p in sell_signals],
                symbol="triangle",
                symbol_rotate=180,
                symbol_size=14,
                itemstyle_opts=opts.ItemStyleOpts(color="red"),
                label_opts=opts.LabelOpts(is_show=False),
            )
        )

    chart.render("obv_signals.html")
    print("生成成功：obv_signals.html")


if __name__ == '__main__':
    stock_name = "iren"
    end_date = "2024-12-31"
    df = pd.read_csv(glob.glob(f"output/rsi_union/2024/{end_date}/{stock_name}/part-00000-*-c000.csv")[0])
    print(df)
    df, buys, sells = calc_obv_signals(df)
    plot_obv_signals(df)