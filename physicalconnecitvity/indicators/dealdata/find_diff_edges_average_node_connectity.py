#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/20 13:27
# @Author  : wuhao
# @Email   : guess?????
# @File    : find_diff_edges.py

import matplotlib
import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns
# coding=utf-8
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import FuncFormatter, MaxNLocator
# 根据路径画图
from numpy import array
from sklearn.preprocessing import MinMaxScaler
# 根据路径画图 加权的
def drawpicture(filePath):
    """
    输入文件路径最后绘制成图G
    """
    global dataMiga
    G = nx.Graph()
    try:
        dataMiga = pd.read_csv(filePath)
    except Exception as problem:
        print("error根据路径画图出现问题：", problem)
    # 得到每一行的数据
    edge_data_info = []
    for row in dataMiga.itertuples():
        city_name = getattr(row, "city_name")
        city_id_name = getattr(row, "city_id_name")
        edge_weight = getattr(row, "num")
        hang = []
        # 添加节点 两个 是有向的
        hang.append(city_name)
        hang.append(city_id_name)
        # 添加边的信息
        weight = {}
        weight["weight"] = edge_weight
        hang.append(weight)
        edge_data_info.append(hang)
        # G.add_edges_from([(city_name, city_id_name)])
        # G.add_weighted_edges_from([(city_name, city_id_name, weight["weight"]=)
    G.add_edges_from(edge_data_info)
    return G
last_end_filename = "0101_0102data.csv"
average_node_connect = [1.4870034729759063, 1.1694896304991895, 1.9654004532053313, 2.460462640340689, 2.2954392541330257, 2.133976964769648, 2.1158536585365852, 2.397018970189702, 2.4661246612466123, 2.330401306011062, 2.5040650406504064, 2.340349865436371, 2.319928377855207, 2.102424506387921, 2.046660656416754, 2.0558704453441297, 2.0200889547813197, 2.123739418476261, 2.1233012107734126, 2.206821248926512, 2.4757681343047198, 2.274457250067006, 1.9691870521373858, 1.5212740544127406, 0.5172706267731274, 1.275126333520494, 0.6313528575160363, 0.46736353077816495, 0.20473225404732254, 0.1962962962962963, 0.17726671953476078, 0.09968173902600132, 0.18638158232066862, 0.09321116802539499, 0.056896551724137934, 0.05971223021582734, 0.06380441264162194, 0.06544049047047848, 0.06831955922865014, 0.04908956692913386, 0.053082795067527895, 0.04677871148459384, 0.0464213631423692, 0.04104683195592287, 0.03811808609889378, 0.039595499216635806, 0.04130465745620282, 0.06420650451961607, 0.06434004474272931, 0.07976889385891343, 0.08896658896658896, 0.0936277892799632, 0.15522054718034617, 0.16099962839093274, 0.25607142857142856, 0.24825396825396825, 0.2773062139654068, 0.29035874439461884, 0.28700341146693076, 0.34024823318448716, 0.3200075287031809, 0.2806251436451391, 0.3064806669180177, 0.35378176129877814, 0.348559486490521, 0.35835075749238837, 0.3386433897072195, 0.32532360723735965, 0.31739811912225707, 0.34518571943743237, 0.39993363198938114, 0.4697009272561055, 0.5070916334661355, 0.562905317769131, 0.8031852321056918, 0.5842087935111191, 0.5427261484631858, 0.5513513513513514, 0.5060396010646077, 0.9045254646049085, 1.140139401394014, 1.097688040325533, 1.0023876709355328, 0.9328927440451604, 1.1507759930540482, 1.139449747965419, 0.9835210564278977, 0.9993115792372298, 1.187594964184936, 1.1987790311877904, 1.294313644499518, 1.1238471673254282, 0.5881612586037365, 0.737610091058367, 1.3503309214361647, 1.367514094245293, 0.701803101334295, 0.6823640127987954, 0.8905579399141631, 0.26164514586322335, 0.8371236386931454, 1.219682852220386, 1.297991967871486, 1.3261490758754864, 1.289255675709859, 1.3375298804780877, 1.2931314741035858, 1.3151807228915662, 1.1920464934047277, 1.320035548533623, 1.295860862806063, 1.2725058424673314, 1.2071897425432778, 1.0032775453277545, 1.2820841973601922, 1.3184342589494815, 1.297223592966782, 1.258193445243805, 1.4403660396542959, 1.3906810035842294, 1.4472606246799795, 2.797691637630662, 2.449343638817323, 2.2093485461906512]
# 数据归一化
tool = MinMaxScaler(feature_range=(0, 1))
# 平均点连通性  归一化
averagenodeconnectivity = tool.fit_transform(array(average_node_connect).reshape(-1,1)).tolist()
# order = ['city_name', 'citye_id_name', 'value', ]

#原始网路



filepath_front ="D:\\04python project\\01-爬虫-爬取百度迁徙数据\\physicalconnecitvity\\indicators\\data\\average_node_connectiy\\"
fileNamePath_one = "F:\\01大连民族\\百度迁徙爬取和数据\\百度迁徙数据-final\\03将两个In和Out相同行合并_最终数据\\"
# '0101-0102data_removeEdges.csv',  '0101-0102data_addEdges.csv' ,  "20200101finalData.csv",
remove_edge_list_diffedge =['0102-0103data_removeEdges.csv','0103-0104data_removeEdges.csv','0104-0105data_removeEdges.csv','0107-0108data_removeEdges.csv','0110-0111data_removeEdges.csv','0111-0112data_removeEdges.csv','0120-0121data_removeEdges.csv','0121-0122data_removeEdges.csv']
add_edge_list_diffedge =['0102-0103data_addEdges.csv' , '0103-0104data_addEdges.csv' , '0104-0105data_addEdges.csv' , '0107-0108data_addEdges.csv' , '0110-0111data_addEdges.csv' , '0111-0112data_addEdges.csv', '0120-0121data_addEdges.csv', '0121-0122data_addEdges.csv']
remove_edge_list_origionnet = ["20200102finalData.csv","20200103finalData.csv","20200104finalData.csv","20200107finalData.csv","20200110finalData.csv","20200111finalData.csv","20200120finalData.csv","20200121finalData.csv"]


def get_edgeTo_caculate(listDiffedge_remove,listDiffedge_add,listOrigionnet):
    global G
    for list_diffedge_remove,list_diffedge_add,list_origionnet in zip(listDiffedge_remove,listDiffedge_add,listOrigionnet):
        dataMiga_remove = pd.read_csv(filepath_front + list_diffedge_remove)
        list_edge_impact_remove={}
        list_edge_impact_add={}
        #删除边来计算结果
        if len(dataMiga_remove) != 0: #判断不为空
            for row in dataMiga_remove.itertuples():
                city_name = getattr(row, "city_name_remove")
                city_id_name = getattr(row, "city_id_name_remove")
                G_remove = drawpicture(fileNamePath_one+list_origionnet)
                G_remove.remove_edge(city_name,city_id_name)
                average_connectiy_removeValue = nx.average_node_connectivity(G_remove)
                list_edge_impact_remove[city_name + "-" + city_id_name] = format(average_connectiy_removeValue, '.4f')
            name_remove = ["edges", 'indicator_value']
            finall_indicators_remove = pd.DataFrame(columns=name_remove, data=sorted(list_edge_impact_remove.items(), key=lambda x: x[1],
                                                                       reverse=True))  # 数据有三列，列名分别为one,two,three
            finall_indicators_remove.to_csv(filepath_front+"result\\"+  list_diffedge_remove[:25] + "_finall_indicators.csv", index=False,
                                     header=name_remove,
                                     encoding="utf-8")
        print(list_edge_impact_remove)
        #增加边计算结果
        dataMiga_add = pd.read_csv(filepath_front + list_diffedge_add)
        if len(dataMiga_add) != 0:  # 判断不为空
            for row_new in dataMiga_add.itertuples():
                city_name_new = getattr(row_new, "city_name_add")
                city_id_name_new = getattr(row_new, "city_id_name_add")
                G_add = drawpicture(fileNamePath_one + list_origionnet)
                G_add.add_edges_from([(city_name_new, city_id_name_new)])
                new_average_connectiy_addValue = nx.average_node_connectivity(G_add)
                list_edge_impact_add[city_name_new+"-"+city_id_name_new] = format(new_average_connectiy_addValue, '.4f')
            name_add = ["edges", 'indicator_value']
            finall_indicators_add = pd.DataFrame(columns=name_add, data= sorted(list_edge_impact_add.items(),key = lambda x:x[1],reverse = True))  # 数据有三列，列名分别为one,two,three
            finall_indicators_add.to_csv(filepath_front+"result\\"+list_diffedge_add[:25] + "_finall_indicators.csv", index=False, header=name_add,
                                     encoding="utf-8")
        print(list_edge_impact_add)

get_edgeTo_caculate(remove_edge_list_diffedge,add_edge_list_diffedge,remove_edge_list_origionnet)
