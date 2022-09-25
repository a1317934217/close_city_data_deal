#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/12 19:03
# @Author  : wuhao
# @Email   : guess?????
# @File    : find_edge.py
import networkx as nx
import pandas as pd

def drawpicture(filePath):
    """
    输入文件路径最后绘制成图G
    """
    G = nx.Graph()
    try:
        dataMiga = pd.read_csv(filePath)
    except Exception as problem:
        print("error根据路径画图出现问题：", problem)
    # 得到每一行的数据
    for row in dataMiga.itertuples():
        city_name = getattr(row, "city_name")
        city_id_name = getattr(row, "city_id_name")
        G.add_edges_from([(city_name, city_id_name)])
    return G

lista_all = ["0221","0223","0306","0315"]
listb_all = ["0222","0224","0307","0316"]
filename_path = "D:\\04python project\\01-爬虫-爬取百度迁徙数据\\physicalconnecitvity\\" \
                "indicators\\data\\finall_data\\diff_degree\\"
fileNamePath_one = "F:\\01大连民族\\百度迁徙爬取和数据\\百度迁徙数据-final\\03将两个In和Out相同行合并_最终数据\\"
G_one = drawpicture(fileNamePath_one+"20200315finalData.csv" )
G_two = drawpicture(fileNamePath_one+"20200316finalData.csv" )
print("G_one edges：",len(G_one.edges()))
print("G_one nodes：",len(G_one.nodes()))

print("G_two edges：",len(G_two.edges()))
print("G_two nodes：",len(G_two.nodes()))
S_one = [G_one.subgraph(c).copy() for c in nx.connected_components(G_one)]
print("连通分量：",len(S_one))
# for i in S_one:
#     print("连通分量：",i.edges())
S_two = [G_two.subgraph(c).copy() for c in nx.connected_components(G_two)]
# for i in S_two:
#     print("连通分量：",i.edges())
print("连通分量：",len(S_two))

