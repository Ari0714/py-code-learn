from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Line
from pyecharts.components import Table
from pyecharts.charts import WordCloud
from pyecharts.charts import Pie
from pyecharts.charts import Funnel
from pyecharts.charts import Scatter
from pyecharts.charts import PictorialBar
from pyecharts.options import ComponentTitleOpts
from pyecharts.globals import SymbolType
import json
import pymysql
import pandas as pd


# 1.画出每日的累计确诊病例数和死亡数——>双柱状图
def drawChart_1():
    root = "output/01/part-00000-c56e6277-452d-496c-9680-14291d293847-c000.json"
    date = []
    cases = []
    deaths = []
    with open(root, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line:  # 到 EOF，返回空字符串，则终止循环
                break
            js = json.loads(line)
            date.append(str(js['date']))
            cases.append(int(js['csum']))
            deaths.append(int(js['dsum']))

    d = (
        Bar()
            .add_xaxis(date)
            .add_yaxis("累计确诊人数", cases, stack="stack1")
            .add_yaxis("累计死亡人数", deaths, stack="stack1")
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(title_opts=opts.TitleOpts(title="美国每日累计确诊和死亡人数"))
            .render("output_html/result01.html")
    )


# 2.画出每日的新增确诊病例数和死亡数——>折线图
def drawChart_2():
    root = "output/02/part-00000-6dfdf67b-81f8-4b1f-9df9-c9014f14eeba-c000.json"
    date = []
    cases = []
    deaths = []
    with open(root, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line:  # 到 EOF，返回空字符串，则终止循环
                break
            js = json.loads(line)
            if ('case_up' in js):
                date.append(str(js['date']))
                cases.append(int(js['case_up']))
                deaths.append(int(js['death_up']))

    (
        Line(init_opts=opts.InitOpts(width="1600px", height="800px"))
            .add_xaxis(xaxis_data=date)
            .add_yaxis(
            series_name="新增确诊",
            y_axis=cases,
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值")

                ]
            ),
            markline_opts=opts.MarkLineOpts(
                data=[opts.MarkLineItem(type_="average", name="平均值")]
            ),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="美国每日新增确诊折线图", subtitle=""),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        )
            .render("output_html/result02-1.html")
    )
    (
        Line(init_opts=opts.InitOpts(width="1600px", height="800px"))
            .add_xaxis(xaxis_data=date)
            .add_yaxis(
            series_name="新增死亡",
            y_axis=deaths,
            markpoint_opts=opts.MarkPointOpts(
                data=[opts.MarkPointItem(type_="max", name="最大值")]
            ),
            markline_opts=opts.MarkLineOpts(
                data=[
                    opts.MarkLineItem(type_="average", name="平均值"),
                    opts.MarkLineItem(symbol="none", x="90%", y="max"),
                    opts.MarkLineItem(symbol="circle", type_="max", name="最高点"),
                ]
            ),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="美国每日新增死亡折线图", subtitle=""),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        )
            .render("output_html/result02-2.html")
    )


# 3.画出截止5.19，美国各州累计确诊、死亡人数和病死率--->表格
def drawChart_3():
    root = "output/03/part-00000-0470cdaa-eb37-4485-a219-4ae9c99d8d05-c000.json"
    allState = []
    with open(root, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line:  # 到 EOF，返回空字符串，则终止循环
                break
            js = json.loads(line)
            row = []
            row.append(str(js['state']))
            row.append(int(js['totalCases']))
            row.append(int(js['totalDeaths']))
            row.append(float(js['deathRate']))
            allState.append(row)

    table = Table()

    headers = ["State name", "Total cases", "Total deaths", "Death rate"]
    rows = allState
    table.add(headers, rows)
    table.set_global_opts(
        title_opts=ComponentTitleOpts(title="美国各州疫情一览", subtitle="")
    )
    table.render("output_html/result03.html")


# 4.画出美国确诊最多的10个州——>词云图
def drawChart_4():
    root = "output/04/part-00000-86e47b4a-254b-4856-a928-e5d7ae00f296-c000.json"
    data = []
    with open(root, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line:  # 到 EOF，返回空字符串，则终止循环
                break
            js = json.loads(line)
            row = (str(js['state']), int(js['totalCases']))
            data.append(row)

    c = (
        WordCloud()
            .add("", data, word_size_range=[20, 100], shape=SymbolType.DIAMOND)    # pic distinguish is small  -》 【10，200】
            .set_global_opts(title_opts=opts.TitleOpts(title="美国各州确诊Top10"))
            .render("output_html/result04.html")
    )


# 5.画出美国死亡最多的10个州——>象柱状图
def drawChart_5():
    root = "output/05/part-00000-6ce9648a-8acc-4b37-94f2-e1df040edccf-c000.json"
    state = []
    totalDeaths = []
    with open(root, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line:  # 到 EOF，返回空字符串，则终止循环
                break
            js = json.loads(line)
            state.insert(0, str(js['state']))
            totalDeaths.insert(0, int(js['totalDeaths']))

    c = (
        PictorialBar()
            .add_xaxis(state)
            .add_yaxis(
            "",
            totalDeaths,
            label_opts=opts.LabelOpts(is_show=False),
            symbol_size=18,
            symbol_repeat="fixed",
            symbol_offset=[0, 0],
            is_symbol_clip=True,
            symbol=SymbolType.ROUND_RECT,
        )
            .reversal_axis()
            .set_global_opts(
            title_opts=opts.TitleOpts(title="PictorialBar-美国各州死亡人数Top10"),
            xaxis_opts=opts.AxisOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(
                axistick_opts=opts.AxisTickOpts(is_show=False),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(opacity=0)
                ),
            ),
        )
            .render("output_html/result05.html")
    )


# 6.找出美国确诊最少的10个州——>词云图
def drawChart_6():
    root = "output/06/part-00000-162d73e2-7d65-48d6-a003-2500a2c1dfc9-c000.json"
    data = []
    with open(root, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line:  # 到 EOF，返回空字符串，则终止循环
                break
            js = json.loads(line)
            row = (str(js['state']), int(js['totalCases']))
            data.append(row)

    c = (
        WordCloud()
            .add("", data, word_size_range=[15, 66], shape=SymbolType.DIAMOND)
            .set_global_opts(title_opts=opts.TitleOpts(title="美国各州确诊最少的10个州"))
            .render("output_html/result06.html")
    )


# 7.找出美国死亡最少的10个州——>漏斗图
def drawChart_7():
    root = "output/07/part-00000-7ea10884-dad5-4b0c-afdc-70110999d489-c000.json"
    data = []
    with open(root, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line:  # 到 EOF，返回空字符串，则终止循环
                break
            js = json.loads(line)
            data.insert(0, [str(js['state']), int(js['totalDeaths'])])

    c = (
        Funnel()
            .add(
            "State",
            data,
            sort_="ascending",
            label_opts=opts.LabelOpts(position="inside"),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="找出美国死亡最少的10个州"))
            .render("output_html/result07.html")
    )


# 8.美国的病死率--->饼状图
def drawChart_8():
    root = "output/08/part-00000-e046639e-e126-4de3-9c51-9ff3cbe54b7b-c000.json"
    values = []
    with open(root, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line:  # 到 EOF，返回空字符串，则终止循环
                break
            js = json.loads(line)
            if str(js['state']) == "USA":
                values.append(["Death(%)", round(float(js['deathRate']) * 100, 2)])
                values.append(["No-Death(%)", 100 - round(float(js['deathRate']) * 100, 2)])
    c = (
        Pie()
            .add("", values)
            .set_colors(["black", "orange", "blue", "green", "purple", "brown"])
            .set_global_opts(title_opts=opts.TitleOpts(title="全美的病死率"))
            # .set_global_opts(title_opts=opts.TitleOpts(title="动漫类别占比分析", pos_top='50px'))  调整标题高度
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            .render("output_html/result08.html")
    )


# 9. mr输出 + 旋转
def drawChart_9():
    root = "output/09/part-r-00000"
    date = []
    cases = []
    with open(root, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line:  # 到 EOF，返回空字符串，则终止循环
                break
            strings = line.split('\t')
            date.append(str(strings[0]))
            cases.append(int(float(strings[1])))

    d = (
        Bar()
            .add_xaxis(date)
            .add_yaxis("票价", cases, stack="stack1")
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 45}))
            .set_global_opts(title_opts=opts.TitleOpts(title="第一天最贵票价top10"))
            .render("output_html/result09.html")
    )


# 读取mysql
def get_db_df(table_name):
    # host表示ip地址，user表示用户名，passwd表示密码，db表示数据库名称
    conn = pymysql.connect(host="hdp", user='root', passwd='111111', db='test', charset="utf8")
    sql_query = "select * from {}".format(table_name)
    df = pd.read_sql(sql_query, con=conn)
    conn.close()
    return df


def drawChart_10():
    allState = []
    df1 = get_db_df('test8')
    for i in zip(df1['name'], df1['author']):
        row = (str(i[0]), str(i[1]))
        allState.append(row)

    table = Table()
    headers = ["name", "author"]
    rows = allState
    table.add(headers, rows)
    table.set_global_opts(
        title_opts=ComponentTitleOpts(title="询评价人数超过200人的曲名与作者信息", subtitle="")
    )
    table.render("output_html/result10.html")


# 11. 散点
# 北京用电量随月份变化分析
def drawChart_11():
    root = "output/03/part-00000-2f6cb13c-1d91-4951-9528-e32a36884393-c000.json"
    date = []
    cases = []
    with open(root, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line:  # 到 EOF，返回空字符串，则终止循环
                break
            js = json.loads(line)
            date.append(str(js['month']))
            cases.append(int(js['avg_load']))

    d = (
        Scatter()
            .add_xaxis(date)
            .add_yaxis("用电量", cases)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(title_opts=opts.TitleOpts(title="北京用电量随月份变化分析"))
            .render("output_html/result03.html")
    )


if __name__ == '__main__':
    # drawChart_1()
    # drawChart_2()
    # drawChart_3()
    # drawChart_4()
    # drawChart_5()
    # drawChart_6()
    # drawChart_7()
    # drawChart_8()

    # mr输出 + 旋转
    drawChart_9()

    # 读取mysql
    # drawChart_10()
