# coding:utf-8
"""
@file: caculate_all_indicort_acedamic.py
@author: wu hao
@time: 2023/3/14 10:28
@env: 封城数据处理
@desc:
@ref:
"""
import csv
import datetime
import os

import matplotlib


from networkx.algorithms import approximation as approx
import networkx as nx
import numpy as np
import pandas as pd
from math import e
from math import log
from tqdm import tqdm

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter, MaxNLocator
from tqdm import tqdm
import numpy as np
from numpy import array
from sklearn.preprocessing import MinMaxScaler
import ast
import json



# 获取时间列表
def getdaylist(begin, end):
    """
    获取时间列表
    """
    beginDate = datetime.datetime.strptime(str(begin), "%Y%m%d")
    endDate = datetime.datetime.strptime(str(end), "%Y%m%d")
    dayList = []
    while beginDate <= endDate:
        dayList.append(datetime.datetime.strftime(beginDate, "%Y%m%d"))
        beginDate += datetime.timedelta(days=+1)
    return dayList


# file_path = "F:/封城数据处理/封城数据/石家庄/石家庄四阶/garbage_self_network/deal_01/in/"


listXData = getdaylist(20210101,20210508)



# 根据路径画图
def drawpicture(filePath):
    """
    输入文件路径最后绘制成图G
    """
    global dataMiga
    G = nx.Graph()
    # G.add_nodes_from(nodes_list_one)
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



#(1) 计算平均点连通性
def averagenodeconnectivity(file_path):
    """
    返回绘制图表的
    X轴：日期
    Y轴：平均点连通性
    """

    listAverageNodeConnectivity = []
    for i in tqdm (range(len(listXData)),desc="平均点连通性进度",total=len(listXData)):
        # 循环画图
        try:
            filePathInMethon = file_path + listXData[i] +"_.csv"
            G = drawpicture(filePathInMethon)

        except Exception as problem:
            print("((平均点连通性) error打开迁徙文件出问题：", problem)
        else:
                listAverageNodeConnectivity.append((nx.average_node_connectivity(G)))
    # print("平均点连通性： ", listAverageNodeConnectivity)
    return listAverageNodeConnectivity



# (2)计算边数量
def edge_number(file_path):
    """
    返回绘制图表的
    X轴：日期
    Y轴：平均点连通性
    """
    list_edge_number = []
    for i in range(len(listXData)):
        # 循环画图
        try:
            filePathInMethon = file_path + listXData[i] +"_.csv"
            G = drawpicture(filePathInMethon)
        except Exception as problem:
            print("((边数量) error打开迁徙文件出问题：", problem)
        else:
            list_edge_number.append(len(G.edges()))
    # print("边数量： ", list_edge_number)
    return list_edge_number


# (3)计算自然连通性
def naturecconnectivity(G):
    """
    返回绘制图表的
    X轴：日期
    Y轴：自然连通度数值
    """
    # 生成邻接矩阵 直接转为稠密矩阵
    Gadjacency = np.array(nx.adjacency_matrix(G).todense())
    # 求特征值和特征向量
    eigenvalue, featurevector = np.linalg.eig(Gadjacency)
    # 取到所有点
    nodes = len(G.nodes())
    # 定义分子
    molecular = 0
    for eigenvalueNeed in eigenvalue:
        # 开始求自然连通度 ln()里的分子
        molecular = molecular + e ** eigenvalueNeed
    # 自然连通度的值
    algebraicConnectivityValue = log(molecular/nodes, e)

    return algebraicConnectivityValue



# (4)计算点连通性(单个点)
def node_connectivity(file_path):
    """
    返回绘制图表的
    X轴：日期
    Y轴：平均点连通性
    """

    listAverageNodeConnectivity = []
    for i in tqdm (range(len(listXData)),desc="点连通性进度",total=len(listXData)):
        # 循环画图
        try:
            filePathInMethon = file_path + listXData[i] +"_.csv"
            G = drawpicture(filePathInMethon)

        except Exception as problem:
            print("点连通性 error打开迁徙文件出问题：", problem)
        else:
                listAverageNodeConnectivity.append((nx.node_connectivity(G)))
    # print("点连通性（单独）： ", listAverageNodeConnectivity)



# (5)计算 平均最短路径长度
def average_short_length(G):
    S = [G.subgraph(c).copy() for c in nx.connected_components(G)]
    AEC_LastValue =0
    for C in (G.subgraph(c).copy() for c in nx.connected_components(G)):
        AEC_LastValue = AEC_LastValue + nx.average_shortest_path_length(C)
    return AEC_LastValue / len(S)



# (6)计算 代数连通性
def algebraic_connectivity(file_path):
    algebraic_connectivity_list = []
    for i in tqdm(range(len(listXData)), desc="代数连通性 进度", total=len(listXData)):
        # 循环画图
        try:
            filePathInMethon = file_path + listXData[i] + "_.csv"
            G = drawpicture(filePathInMethon)

        except Exception as problem:
            print("代数连通性   error打开迁徙文件出问题：", problem)
        else:

            algebraic_connectivity_list.append(nx.algebraic_connectivity(G))

    print("代数连通性",algebraic_connectivity_list)


# (7)计算  连通性损失指标
def connectivity_loss(G):
    """
    连通性损失指标计算
    输入为图
    """


    allNodes = array(G.nodes())
    # 定义分母
    deniminator = 0
    for i in range(0, G.number_of_nodes()):
        # 定义Ni
        numnumber = 0
        for j in range(0, G.number_of_nodes()):
            connectiveOrNone = nx.has_path(G, allNodes[i], allNodes[j])
            if connectiveOrNone:
                numnumber += 1
        twoNodesLoss = 1 - (numnumber / len(allNodes))
        deniminator = deniminator + twoNodesLoss
    connectivityLoss = deniminator / len(allNodes)

    return connectivityLoss


# (8)计算  最大组件大小
def size_of_largest_component(G):
    S = [G.subgraph(c).copy() for c in nx.connected_components(G)]
    return len(S[0])



# # (9)计算连通分量数量
def number_of_connected_components():
    """
    返回绘制图表的
    X轴：日期
    Y轴：点连通性
    """
    list_number_of_connected_components_everyDay = []
    list_number_of_connected_components_everyDay_superNode = []
    for i in range(len(listXData)):
        # 循环画图
        try:
            filePathInMethon = fileNamePath + listXData[i] + "finalData.csv"
            print(filePathInMethon)
            G = drawpicture(filePathInMethon)
            for city_want in nodeList:
                G.add_edges_from([(city_want, "超级节点")])
            S = [G.subgraph(c).copy() for c in nx.connected_components(G)]
        except Exception as problem:
            print("(连通分量数量) error打开迁徙文件出问题：", problem)
        else:
            list_number_of_connected_components_everyDay.append(len(S))
            list_number_of_connected_components_everyDay_superNode.append(len(S))
    print("连通分量数量列表为：", list_number_of_connected_components_everyDay_superNode)
    # 画图 设置X轴显示效果
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # 为了设置x轴时间的显示
    def format_fn(tick_val, tick_pos):
        if int(tick_val) in range(len(listXData)):
            return listXData[int(tick_val)]
        else:
            return ''

    ax.xaxis.set_major_formatter(FuncFormatter(format_fn))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # plt.ylim((-5, 40))
    # 横坐标每个值旋转90度
    # plt.xticks(rotation=90)
    # 设置Mac上的字体
    # font = FontProperties(fname='/Library/Fonts/Arial Unicode.ttf')
    font = matplotlib.font_manager.FontProperties(
        fname='C:\\Windows\\Fonts\\SimHei.ttf')
    # 坐标轴ticks的字体大小
    plt.tick_params(labelsize=5)
    plt.yticks(fontsize=10)
    plt.xticks(fontsize=7)
    plt.xlabel('日期', FontProperties=font)
    plt.ylabel('连通分量数量', FontProperties=font)
    plt.title('百度迁徙2020上半年连通分量数量折线图', FontProperties=font)
    ax.plot(listXData, list_number_of_connected_components_everyDay,"m.-", linewidth=1, color='blue')
    plt.show()












def get_all_indicators(list_time,file_origion):
    """
    生成最终指标和经济汇总的数据集
    :param list_time:
    :param file_origion:
    :return:
    """
    file_order = ["City_name", 'Average_node_connectivity', "City_degree", "Edge_number",
                  "Nature_connectivity", "Average_short_length", "Algebraic_connectivity",
                  "node_connectivity","connectivity_loss","size_of_largest_component","eco_value"]
    with open(file_origion + "indicator_data_end.csv", 'w', encoding="utf-8", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, file_order)
        writer.writeheader()
        data_eco = pd.read_csv(file_origion  + "主要城市月度价格.csv")
        for time_alone in tqdm(list_time,desc="指标处理进度：", total=len(list_time)):
            #定位到网络连边数据
            data_graph = pd.read_csv(file_origion + time_alone + "_AroundCityName.csv")
            for row_city in data_graph.iterrows():

                # 定位到城市名称
                cityName = row_city[1]["city_name"]
                # 有了城市名称可以定位到经济数据
                eco_value = data_eco.loc[cityName, time_alone]


                #处理网络边集
                edges = row_city[1]["city_around_list_name"]
                list_edges = ast.literal_eval(edges)
                #返回网络
                G = drawpicture(list_edges)


                #求网络参数
                #平均点连通性
                Average_node_connectivity = nx.average_node_connectivity(G)
                #城市度
                City_degree = len(G.edges(cityName))
                #边数量
                Edge_number = len(G.edges())
                #计算自然连通性
                Nature_connectivity =  naturecconnectivity(G)
                #平均最短路径长度
                Average_short_length = average_short_length(G)
                #代数连通性
                Algebraic_connectivity =nx.algebraic_connectivity(G)
                #点连通性
                node_connectivity =nx.node_connectivity(G)
                #连通性损失
                connectivity_loss_value =connectivity_loss(G)
                #最大组件大小
                size_of_largest_component_value = size_of_largest_component(G)

                row = {"City_name": cityName,
                       "Average_node_connectivity": Average_node_connectivity,
                       "City_degree": City_degree,
                       "Edge_number": Edge_number,
                       "Nature_connectivity": Nature_connectivity,
                       "Average_short_length": Average_short_length,
                       "Algebraic_connectivity": Algebraic_connectivity,
                       "node_connectivity": node_connectivity,
                       "connectivity_loss": connectivity_loss_value,
                       "size_of_largest_component": size_of_largest_component_value,
                        "eco_value":eco_value}
                writer.writerow(row)












if __name__ == '__main__':
    # 时间序列
    list_time = ['20230112', '20221212', '20221112', '20221012', '20220912', '20220812', '20220712', '20220612',
                 '20220512', '20220412', '20220312', '20220212', '20220112', '20211212', '20211112', '20211012',
                 '20210912', '20210812', '20210712', '20210612', '20210512', '20210412', '20210312', '20210212',
                 '20210112', '20201212', '20201112', '20201012']

    # 需要找一节自我中心的城市的城市
    list_cityName = ['北京', '上海', '南京', '广州', '深圳', '重庆', '成都','天津', '石家庄', '太原', '呼和浩特', '沈阳', '大连', '长春', '哈尔滨', '杭州', '宁波', '合肥', '福州', '厦门', '南昌', '济南', '青岛',
                     '郑州', '武汉', '长沙', '南宁', '海口', '贵阳', '昆明', '拉萨', '西安', '兰州', '西宁', '银川', '乌鲁木齐']

    # 寻找构建网络的文件
    file_origion = "F:/封城数据处理/paper_supplement_experiment/data/city_around_by_time/"

    # 寻找构建网络的文件
    # file_migration = "F:/封城数据处理/paper_supplement_experiment/data/merge_complete/"


    # 生成的一阶自我中心网络城市集合
    file_path_around_city_first = "F:/封城数据处理/paper_supplement_experiment/data/city_around_by_time/"

    get_all_indicators(list_time,file_origion)