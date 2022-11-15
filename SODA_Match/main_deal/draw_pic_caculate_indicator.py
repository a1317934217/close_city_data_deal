# coding:utf-8
"""
@file: draw_pic_caculate_indicator.py
@author: wu hao
@time: 2022/10/20 11:06
@env: 封城数据处理
@desc:
@ref:
"""
import datetime

import matplotlib


from networkx.algorithms import approximation as approx
import networkx as nx
import numpy as np
import pandas as pd
from math import e
from math import log
from tqdm import tqdm

import matplotlib
import pandas as pd
import csv
import datetime
import networkx as nx
import numpy as np
import pandas as pd
# coding=utf-8
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import FuncFormatter, MaxNLocator
import matplotlib.pyplot as plt


# 根据路径画图
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
    for row in dataMiga.itertuples():
        city_name = getattr(row, "段起点")
        city_id_name = getattr(row, "段止点")
        G.add_edges_from([(city_name, city_id_name)])

    return G


# 计算平均点连通性
def averagenodeconnectivity(G):
    return nx.average_node_connectivity(G)

# 计算自然连通性
def naturecconnectivity(G):


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
    return  algebraicConnectivityValue

# 计算全局效率
def globalefficiency(G):
    return nx.global_efficiency(G)

# 获取连通性损失指标
def connectivityloss(G):
    """
    连通性损失指标计算
    输入为图
    """
    # 获取到所有节点信息
    allNodes = np.array(G.nodes())
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


if __name__ == '__main__':
    file_name_baoshan = "F:/封城数据处理/SODA_Match/data/baoshan.csv"
    file_name_pudong = "F:/封城数据处理/SODA_Match/data/pudong.csv"
    G_baoshan  = drawpicture(file_name_baoshan)
    G_pudong  = drawpicture(file_name_pudong)

    print("宝山",G_baoshan)
    print("浦东",G_pudong)

    # print("宝山平均点连通性", averagenodeconnectivity(G_baoshan))
    # print("浦东平均点连通性", averagenodeconnectivity(G_pudong))
    #
    # print("宝山自然连通性", naturecconnectivity(G_baoshan))
    # print("浦东自然连通性", naturecconnectivity(G_pudong))
    #
    # print("宝山全局效率", globalefficiency(G_baoshan))
    # print("浦东全局效率", globalefficiency(G_pudong))

    # print("宝山连通性损失指标", connectivityloss(G_baoshan))
    # print("浦东连通性损失指标", connectivityloss(G_pudong))



    plt.rcParams['font.sans-serif'] = ['SimHei']


    # pos_one = nx.spring_layout(G_baoshan)
    # nx.draw(G_baoshan, pos_one, font_size=12, with_labels=False, node_color="red", node_size=3)
    #
    # plt.subplot(122)
    pos_two = nx.spring_layout(G_pudong)
    nx.draw(G_pudong, pos_two, font_size=12, with_labels=False, node_color="red", node_size=3)
    #
    plt.show()




