#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/15 23:00
# @Author  : wuhao
# @Email   : guess?????
# @File    : GeoDemo.py
from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType, SymbolType

c = (
    Geo()
    .add_schema(
        maptype="china",
        itemstyle_opts=opts.ItemStyleOpts(color="white", border_color="#111"),
    )
    # .add(
    #     "",
    #     [("广州", 55), ("北京", 66), ("杭州", 77), ("重庆", 88)],
    #     type_=ChartType.EFFECT_SCATTER,
    #     color="white",
    # )
    .add(
        "geo",
        [("广州", "上海"), ("广州", "北京"), ("广州", "杭州"), ("广州", "重庆")],
        type_=ChartType.LINES,
        effect_opts=opts.EffectOpts(
            symbol=SymbolType.ARROW, symbol_size=6, color="blue"
        ),
        is_polyline=True,
        linestyle_opts=opts.LineStyleOpts(curve=0.2, opacity = 0.5,type_ = 'solid'),
    )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(title_opts=opts.TitleOpts(title="Geo-Lines-background"))
    .render("geo_lines_background.html")
)
