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

# 10. 读取mysql
def get_db_df(table_name):
    # host表示ip地址，user表示用户名，passwd表示密码，db表示数据库名称
    conn = pymysql.connect(host="hdp", user='root', passwd='111111', db='test', charset="utf8")
    sql_query = "select * from {}".format(table_name)
    df = pd.read_sql(sql_query, con=conn)
    conn.close()
    return df

# 直方图：各学历平均工资(X轴学历、Y轴该学历的平均工资)
def drawChart_1():
    root = "output/01/part-00000-dd69c7e3-123b-4bcb-a0a0-92b9a49bbe98-c000.json"
    date = []
    cases = []
    with open(root, 'r',encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line:  # 到 EOF，返回空字符串，则终止循环
                break
            js = json.loads(line)
            date.append(str(js['education']))
            cases.append(float(js['avg_salary']))

    d = (
        Bar()
            .add_xaxis(date)
            .add_yaxis("平均工资", cases, stack="stack1")
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(title_opts=opts.TitleOpts(title="各学历平均工资"))
            .render("output_html/result1.html")
    )


# 折线图：各城市平均工资走势(X轴 10大城市、Y轴 该城市对应的平均工资)
def drawChart_2():
    root = "output/02/part-00000-bedb1200-1b38-4ee3-986c-505d4052924a-c000.json"
    date = []
    cases = []
    with open(root, 'r',encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line:  # 到 EOF，返回空字符串，则终止循环
                break
            js = json.loads(line)
            date.append(str(js['city']))
            cases.append(float(js['avg_salary']))

    (
        Line(init_opts=opts.InitOpts(width="1600px", height="800px"))
            .add_xaxis(xaxis_data=date)
            .add_yaxis(
            series_name="工资",
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
            title_opts=opts.TitleOpts(title="各城市平均工资走势", subtitle=""),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        )
            .render("output_html/result2.html")
    )


# 饼图：各岗位招聘数量占比分析(数据分析师、机器学习工程师、数据挖掘工程师等）
def drawChart_3():
    root = "output/03/part-00000-e591f3bf-e88f-47d0-a01e-6eb655c6a61c-c000.json"
    values = []
    with open(root, 'r',encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line:                            # 到 EOF，返回空字符串，则终止循环
                break
            js = json.loads(line)
            values.append([(js['position_name']),(js['cnt'])])
    c = (
    Pie()
    .add("", values)
    .set_colors(["orange","red","blue","green"])
    .set_global_opts(title_opts=opts.TitleOpts(title="各岗位招聘数量占比分析"))
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    .render("output_html/result3.html")
    )


if __name__ == '__main__':
    drawChart_1()
    drawChart_2()
    drawChart_3()

