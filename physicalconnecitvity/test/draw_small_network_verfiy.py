#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/1/10 19:35
# @Author  : wuhao
# @Email   : guess?????
# @File    : drawpicture.py
import networkx as nx

from math import e, log
from matplotlib import pyplot as plt
import numpy as np
def drawPic_one():
    G = nx.Graph()
    G.add_node("A",desc="A")
    G.add_node("B",desc="B")
    G.add_node("C",desc="C")
    G.add_node("D",desc="D")
    G.add_node("E",desc="E")
    G.add_node("F",desc="F")
    G.add_node("G",desc="G")
    G.add_edges_from([("A","B") ,("A" ,"D") ,("C" ,"B") ,("C" ,"D"),("B" ,"D"),("E" ,"F"),("G" ,"F"),("D" ,"E"),("G" ,"A")])

    pos = nx.circular_layout(G)
    nx.draw(G,pos,node_size=1000)
    mode_labels = nx.get_node_attributes(G,'desc')
    nx.draw_networkx_labels(G,pos,labels=mode_labels,font_size=25,font_color="white")
    plt.show()
    return G
def drawPic_Two():
    G = nx.Graph()
    G.add_node("A",desc="A")
    G.add_node("B",desc="B")
    G.add_node("C",desc="C")
    G.add_node("D",desc="D")
    G.add_node("E",desc="E")
    G.add_node("F",desc="F")
    G.add_node("G",desc="G")
    G.add_edges_from([("A","B") ,("A" ,"D") ,("C" ,"B") ,("C" ,"D"),("B" ,"D"),("E" ,"F"),("G" ,"F")])

    pos = nx.circular_layout(G)
    nx.draw(G,pos,node_size=1000)
    mode_labels = nx.get_node_attributes(G,'desc')
    nx.draw_networkx_labels(G,pos,labels=mode_labels,font_size=20,font_color="white")
    plt.show()
    return G
def drawPic_Three():
    G = nx.Graph()
    G.add_node("A",desc="A")
    G.add_node("B",desc="B")
    G.add_node("C",desc="C")
    G.add_node("D",desc="D")
    G.add_node("E",desc="E")
    G.add_node("F",desc="F")
    G.add_node("G",desc="G")
    G.add_edges_from([("A","B") ,("A" ,"D") ,("C" ,"B") ,("C" ,"D"),("B" ,"D"),("E" ,"F"),("H" ,"F"),("D" ,"E"),("G" ,"A")])

    pos = nx.circular_layout(G)
    nx.draw(G,pos,node_size=20)
    mode_labels = nx.get_node_attributes(G,'desc')
    nx.draw_networkx_labels(G,pos,labels=mode_labels,font_size=10,font_color="white")
    plt.show()
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
# 全连通
G_one = drawPic_one()
# 不连通
G_two = drawPic_Two()


# AEC_LastValue_one =0
# for C_one in (G_one.subgraph(c).copy() for c in nx.connected_components(G_one)):
#     AEC_LastValue_one = AEC_LastValue_one + nx.average_shortest_path_length(C_one)
# print("G1平均最短路径长度:",AEC_LastValue_one)
# AEC_LastValue_two =0
# for C_two in (G_two.subgraph(c).copy() for c in nx.connected_components(G_two)):
#     AEC_LastValue_two = AEC_LastValue_two + nx.average_shortest_path_length(C_two)
# print("G1平均最短路径长度:",AEC_LastValue_two)



# G_one_algebaric = nx.average_node_connectivity(G_one)
# G_two_algebaric = nx.average_node_connectivity(G_two)
# print("G1平均点连通性:",G_one_algebaric)
# print("G2平均点连通性：",G_two_algebaric)


S_one = [G_one.subgraph(c).copy() for c in nx.connected_components(G_one)]
print("G1最大连通组件:",len(S_one[0]))
S_two = [G_two.subgraph(c).copy() for c in nx.connected_components(G_two)]
print("G2最大连通组件:",len(S_two[0]))
