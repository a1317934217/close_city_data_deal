 #!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/10 8:32 下午
# @Author  : wuhao
# @Site    : 
# @File    : maptest.py
# @Software: PyCharm
import pyecharts

import pandas as pd  #pandas是强大的数据处理库


from pyecharts.charts import Bar, Pie, Map, WordCloud
import webbrowser
from pyecharts import options as opts
from pyecharts.charts import Geo

# 世界地图数据
value = [95.1, 23.2, 43.3, 66.4, 88.5]
attr = ["China", "Canada", "Brazil", "Russia", "United States"]

# 省和直辖市
province_distribution = {'河南': 45.23, '北京': 37.56, '河北': 21, '辽宁': 12, '江西': 6, '上海': 20, '安徽': 10, '江苏': 16, '湖南': 9,
                         '浙江': 13, '海南': 2, '广东': 22, '湖北': 8, '黑龙江': 11, '澳门': 1, '陕西': 11, '四川': 7, '内蒙古': 3, '重庆': 3,
                         '云南': 6, '贵州': 2, '吉林': 3, '山西': 12, '山东': 11, '福建': 4, '青海': 1, '舵主科技，质量保证': 1, '天津': 1,
                         '其他': 1}
provice = list(province_distribution.keys())
values = list(province_distribution.values())

# 城市 -- 指定省的城市 xx市
city = ['郑州市', '安阳市', '洛阳市', '濮阳市', '南阳市', '开封市', '商丘市', '信阳市', '新乡市']
values2 = [1.07, 3.85, 6.38, 8.21, 2.53, 4.37, 9.38, 4.29, 6.1]

# 区县 -- 具体城市内的区县  xx县
quxian = ['夏邑县', '民权县', '梁园区', '睢阳区', '柘城县', '宁陵县']
values3 = [3, 5, 7, 8, 2, 4]



# maptype='china' 只显示全国直辖市和省级
# 数据只能是省名和直辖市的名称
# map = Map("中国地图",'中国地图', width=1200, height=600)
# map.add("", provice, values, visual_range=[0, 50],  maptype='china', is_visualmap=True,
#     visual_text_color='#000')
# map.show_config()
# map.render(path="04-01中国地图.html")



g = (Geo(
    init_opts=opts.InitOpts(width="900px",height="900px",page_title="12345",bg_color="#404a59")#颜色是str的16进制或英文都可以
).add_schema(
        maptype="china",#地图类型
        itemstyle_opts=opts.ItemStyleOpts(
            color="#323c48"#背景颜色
         , border_color="white")#边界线颜色
        ))
g.add_coordinate("第一个坐标点",114.9175,36.3622222)
g.add_coordinate("第二个坐标点",121.7825,31.1705555)

g.add(series_name='系列1'#系列名
      , data_pair=[("第一个坐标点",'非常的大')]#系列里需要的点用列表框住多个元组达到批量输入的效果[(坐标点1，坐标点1的值),(坐标点2，坐标点2的值),(坐标点3，坐标点3的值)]
      , symbol_size=35#系列内显示点的大小
      , color="black"
      ,is_selected=True
    )
g.add(series_name='系列2'
      , data_pair=[("第二个坐标点",'非常的小')]
      , symbol_size=5
      , color="white"
      ,is_selected=False
    )
g.set_series_opts(
    label_opts=opts.LabelOpts(
        is_show=False
    ))
g.set_global_opts(
    title_opts=opts.TitleOpts(
        title='12345678767545323',#主标题内容
        subtitle='324567876564534',#副标题内容
        item_gap=15,#主副标题的间距
        title_textstyle_opts=opts.TextStyleOpts(
            color="white",#主标题颜色
            font_weight="bolder",#主标题加粗
            font_size=40#主标题字体大小
        ),
        subtitle_textstyle_opts=opts.TextStyleOpts(
            color='gray',#副标题颜色
            font_weight="bolder",#副标题加粗
            font_size=15))#副标题副标题字体大小
        ,legend_opts=opts.LegendOpts(pos_right="10px",inactive_color="white",textstyle_opts=opts.TextStyleOpts(color="orange"))
    )
result=g.render()#会在你py文件同目录下生成一个html文件，也可在括号内输入保存路径，用浏览器打开html文件可以查看
webbrowser.open(result)


