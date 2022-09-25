#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/1/5 16:32
# @Author  : wuhao
# @Email   : guess?????
# @File    : finddealcity.py
import networkx as nx
from networkx.tests.test_convert_pandas import pd

moveIn = pd.read_csv("F:\\01大连民族\\百度迁徙爬取和数据\\百度迁徙数据-final\\in\\20200101.csv")
G = nx.Graph()

# 得到每一行的数据
for row in moveIn.itertuples():
    city_name = getattr(row, "city_name")
    city_id_name = getattr(row, "city_id_name")
    G.add_edges_from([(city_name, city_id_name)])
