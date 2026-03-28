import glob

import pandas as pd
import numpy as np
from pyecharts.charts import Line, Scatter
from pyecharts import options as opts

import numpy as np
import pandas as pd
from pyecharts.charts import Kline, Line, Scatter, Grid
from pyecharts import options as opts


def supertrend_chart(df, atr_period=10, multiplier=3, outfile="supertrend.html"):
    df = df.copy()
    hl2 = (df["high"] + df["low"]) / 2

    # === ATR ===
    df["tr"] = np.maximum(df["high"] - df["low"],
                          np.maximum(abs(df["high"] - df["close"].shift()),
                                     abs(df["low"] - df["close"].shift())))
    df["atr"] = df["tr"].rolling(atr_period).mean()

    upper_band = hl2 + multiplier * df["atr"]
    lower_band = hl2 - multiplier * df["atr"]

    supertrend = [np.nan] * len(df)
    trend = [1] * len(df)      # 1=多头  -1=空头

    supertrend[atr_period] = lower_band.iloc[atr_period]

    # === SuperTrend 主循环（无重绘）===
    for i in range(atr_period + 1, len(df)):
        if df["close"].iloc[i] > supertrend[i - 1]:
            trend[i] = 1
        elif df["close"].iloc[i] < supertrend[i - 1]:
            trend[i] = -1
        else:
            trend[i] = trend[i - 1]

        if trend[i] == 1:
            supertrend[i] = max(lower_band.iloc[i], supertrend[i - 1])
        else:
            supertrend[i] = min(upper_band.iloc[i], supertrend[i - 1])

    df["supertrend"] = supertrend
    df["trend"] = trend

    # === 买卖信号 ===
    df["buy"] = np.where(
        (df["trend"] == 1) & (df["trend"].shift() == -1),
        df["low"] * 0.995,
        np.nan
    )
    df["sell"] = np.where(
        (df["trend"] == -1) & (df["trend"].shift() == 1),
        df["high"] * 1.005,
        np.nan
    )

    # 所有展示数据保留 1 位小数（不影响 NaN）
    for col in ["open", "high", "low", "close", "supertrend", "buy", "sell"]:
        if col in df.columns:
            df[col] = df[col].apply(lambda v: round(v, 1) if pd.notna(v) else v)

    # === 图表 X 轴 日期 ===
    x = df["date"].astype(str).tolist()

    # === K 线图 ===
    kline = (
        Kline()
        .add_xaxis(x)
        .add_yaxis("Kline", df[["open","close","low","high"]].values.tolist())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="SuperTrend Strategy"),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
            legend_opts=opts.LegendOpts(pos_left="left")
        )
    )

    # === SuperTrend 线 ===
    st_line = (
        Line()
        .add_xaxis(x)
        .add_yaxis("SuperTrend", df["supertrend"].tolist(),
                   is_smooth=True, linestyle_opts=opts.LineStyleOpts(width=2, color="green"))
    )

    # === 信号图层 ===
    buy_points = df[df["buy"].notna()]
    sell_points = df[df["sell"].notna()]

    buy_scatter = Scatter().add_xaxis(buy_points["date"].tolist()).add_yaxis(
        "BUY", buy_points["buy"].tolist(), symbol="triangle", symbol_size=14,
        itemstyle_opts=opts.ItemStyleOpts(color="green")
    )

    sell_scatter = Scatter().add_xaxis(sell_points["date"].tolist()).add_yaxis(
        "SELL", sell_points["sell"].tolist(), symbol="triangle", symbol_rotate=180, symbol_size=14,
        itemstyle_opts=opts.ItemStyleOpts(color="red")
    )

    chart = kline.overlap(st_line).overlap(buy_scatter).overlap(sell_scatter)

    # === 输出 ===
    grid = Grid()
    grid.add(chart, grid_opts=opts.GridOpts())
    grid.render(outfile)
    print(f"生成成功 → {outfile}")

    return df  # 返回计算结果 DataFrame



# ========== 示例入口 ==========
if __name__ == "__main__":
    # df = pd.read_csv("your_kline.csv")  # 必须包含列：date open high low close volume

    stock_name = "qqq"
    end_date = "2024-12-31"
    df = pd.read_csv(glob.glob(f"output/rsi_union/2024/{end_date}/{stock_name}/part-00000-*-c000.csv")[0])

    supertrend_chart(df)


