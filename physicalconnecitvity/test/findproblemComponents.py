#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/1/8 14:49
# @Author  : wuhao
# @Email   : guess?????
# @File    : findproblemComponents.py
import csv

import networkx as nx
import pandas as pd


# coding=utf-8

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
def get_connect_component_problem():
    """
    查看所有的连通分量
    :return:
    """
    listData20_21 =['20200101', '20200102', '20200103', '20200104', '20200105', '20200106', '20200107', '20200108', '20200109', '20200110', '20200111', '20200112', '20200113', '20200114', '20200115', '20200116', '20200117', '20200118', '20200119', '20200120', '20200121', '20200122', '20200123', '20200124', '20200125', '20200126', '20200127', '20200128', '20200129', '20200130', '20200131', '20200201', '20200202', '20200203', '20200204', '20200205', '20200206', '20200207', '20200208', '20200209', '20200210', '20200211', '20200212', '20200213', '20200214', '20200215', '20200216', '20200217', '20200218', '20200219', '20200220', '20200221', '20200222', '20200223', '20200224', '20200225', '20200226', '20200227', '20200228', '20200229', '20200301', '20200302', '20200303', '20200304', '20200305', '20200306', '20200307', '20200308', '20200309', '20200310', '20200311', '20200312', '20200313', '20200314', '20200315', '20200316', '20200317', '20200318', '20200319', '20200320', '20200321', '20200322', '20200323', '20200324', '20200325', '20200326', '20200327', '20200328', '20200329', '20200330', '20200331', '20200401', '20200402', '20200403', '20200404', '20200405', '20200406', '20200407', '20200408', '20200409', '20200410', '20200411', '20200412', '20200413', '20200414', '20200415', '20200416', '20200417', '20200418', '20200419', '20200420', '20200421', '20200422', '20200423', '20200424', '20200425', '20200426', '20200427', '20200428', '20200429', '20200430', '20200501', '20200502', '20200503']

    field_order_move_in = ["时间","连通分量", '分量的城市']
    with open("D:\\04python project\\01-爬虫-爬取百度迁徙数据\\physicalconnecitvity\\findproblemdata\\findproblemComponents.csv", 'w', encoding="utf-8", newline='') as csvfile:

        writer = csv.DictWriter(csvfile, field_order_move_in)
        writer.writeheader()
        for i in range(len(listData20_21)):
            # 循环画图
            try:
                filePathInMethon = "F:\\01大连民族\百度迁徙爬取和数据\\百度迁徙数据-final\\03将两个In和Out相同行合并_最终数据\\" + listData20_21[i] + "finalData.csv"
                print(filePathInMethon)
                G = drawpicture(filePathInMethon)
            except Exception as problem:
                print("(平均边连通性) error打开迁徙文件出问题：", problem)
            else:
                S = [G.subgraph(c).copy() for c in nx.connected_components(G)]
                for subgraphValue in range(len(S)):
                    print(subgraphValue)
                    row = {"时间":listData20_21[i],"连通分量":subgraphValue+1, "分量的城市": S[subgraphValue].nodes()}
                    writer.writerow(row)

get_connect_component_problem()
