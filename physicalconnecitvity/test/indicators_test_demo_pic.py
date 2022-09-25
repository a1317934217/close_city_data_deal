#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/1/15 16:43
# @Author  : wuhao
# @Email   : guess?????
# @File    : indicators_test_demo_pic.py
import datetime

import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
# coding=utf-8
from math import log, e
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import FuncFormatter, MaxNLocator
# 多重边无向图
from numpy import array
import matplotlib.pyplot as plt
from networkx import nx
import numpy as np
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
    # 作为Y轴
    return algebraicConnectivityValue
def connectivityloss(G):
    """
    连通性损失指标计算
    输入为图
    """
    # 获取到所有节点信息
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
G = nx.Graph()
G.add_node("A", desc="A")
G.add_node("B", desc="B")
G.add_node("C", desc="C")
G.add_node("D", desc="D")
G.add_node("E", desc="E")
# G.add_node("F", desc="F")
# G.add_node("G", desc="G")
G.add_edges_from(
    [("A", "B"), ("A", "D"), ("C", "B"), ("C", "D"),  ("B", "D")])

pos = nx.circular_layout(G)
nx.draw(G,pos,node_size=20)
mode_labels = nx.get_node_attributes(G,'desc')
nx.draw_networkx_labels(G,pos,labels=mode_labels,font_size=10,font_color="white")
plt.show()

# AEC_LastValue_one =0
# for C_one in (G.subgraph(c).copy() for c in nx.connected_components(G)):
#     print(nx.average_shortest_path_length(C_one))

print(nx.average_node_connectivity(G))
#     AEC_LastValue_one = AEC_LastValue_one + nx.average_shortest_path_length(C_one)
# print("G1平均最短路径长度:",AEC_LastValue_one)



