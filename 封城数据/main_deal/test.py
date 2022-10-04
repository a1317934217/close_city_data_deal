# -*- coding: utf-8 -*-
"""
@file: test.py
@author: wu hao
@time: 2022/9/26 10:19
@env: 封城数据处理
@desc:
@ref:
"""
import rpy2.robjects as robjects
import pandas as pd
import networkx as nx
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
import networkx as nx
import matplotlib.pyplot as plt

from nxviz import GeoPlot

reference_file = r"F:\封城数据处理\封城数据\main_deal\data\20210101_merge.csv"
file_name_test = "F:/封城数据处理/封城数据/石家庄/石家庄一阶/garbage_self_network/deal_03/20210101_石家庄.csv"
cc = pd.read_csv(reference_file)
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
        city_name = getattr(row, "city_name")
        city_id_name = getattr(row, "city_id_name")
        G.add_edges_from([(city_name, city_id_name)])
    return G


def fat_tree_topo(n=2):
    """Standard fat tree topology
    n: number of pods
    total n^3/4 servers
    """
    # topo = nx.Graph()
    topo = drawpicture(file_name_test)
    num_of_servers_per_edge_switch = n // 2
    num_of_edge_switches = n // 2
    num_of_aggregation_switches = num_of_edge_switches
    num_of_core_switches = int((n / 2) * (n / 2))

    # generate topo pod by pod
    for i in range(n):
        for j in range(num_of_edge_switches):
            topo.add_node("Pod {} edge switch {}".format(i, j))
            topo.add_node("Pod {} aggregation switch {}".format(i, j))
            for k in range(num_of_servers_per_edge_switch):
                topo.add_node("Pod {} edge switch {} server {}".format(
                    i, j, k))
                topo.add_edge(
                    "Pod {} edge switch {}".format(i, j),
                    "Pod {} edge switch {} server {}".format(i, j, k))

    # add edge among edge and aggregation switch within pod
    for i in range(n):
        for j in range(num_of_aggregation_switches):
            for k in range(num_of_edge_switches):
                topo.add_edge("Pod {} aggregation switch {}".format(i, j),
                              "Pod {} edge switch {}".format(i, k))

    # add edge among core and aggregation switch
    num_of_core_switches_connected_to_same_aggregation_switch = num_of_core_switches // num_of_aggregation_switches
    for i in range(num_of_core_switches):
        topo.add_node("Core switch {}".format(i))
        aggregation_switch_index_in_pod = i // num_of_core_switches_connected_to_same_aggregation_switch
        for j in range(n):
            topo.add_edge(
                "Core switch {}".format(i),
                "Pod {} aggregation switch {}".format(
                    j, aggregation_switch_index_in_pod))

    topo.name = 'fattree'

    return topo

def bcube_topo(k=0, n=13):
    """Standard Bcube topology
    k: layers
    n: num of servers
    total n ^ (k+1) servers
    """
    topo = nx.Graph()
    # topo = drawpicture(file_name_test)
    num_of_servers = n**(k + 1)
    # add server first
    for i in range(num_of_servers):
        topo.add_node("Server {}".format(i))

    # add switch by layer
    num_of_switches = int(num_of_servers / n)
    for i in range(k + 1):
        index_interval = n**i
        num_of_one_group_switches = n**i
        for j in range(num_of_switches):
            topo.add_node("Layer {} Switch {}".format(i, j))
            start_index_server = j % num_of_one_group_switches + (
                j // num_of_one_group_switches) * num_of_one_group_switches * n
            for k in range(n):
                server_index = start_index_server + k * index_interval
                topo.add_edge("Server {}".format(server_index),
                              "Layer {} Switch {}".format(i, j))

    topo.name = 'Bcube'

    return topo





# topo = fat_tree_topo()
# topo = bcube_topo()


G = drawpicture(file_name_test)
# # pos = {}
# pos=nx.spring_layout(G)
# for node in G.nodes():
#     pos[node] = [G.node[node]["x"], G.node[node]["y"]]


# plt.rcParams["font.sans-serif"]=["SimHei"] #设置字体
# plt.rcParams["axes.unicode_minus"]=False #该语句解决图像中的“-”负号的乱码问题
# plt.rcParams['figure.figsize']= (12, 12)
# nx.draw(pos, with_labels=True)
# plt.show()
print(G.nodes())
node = ['廊坊', '北京', '保定', '天津', '张家口', '石家庄', '承德', '唐山', '邯郸', '沧州', '秦皇岛', '邢台', '衡水']

import igraph as ig
g=ig.Graph()
# g.add_vertices(G.nodes())
g.add_vertices(node)
g.add_edges(G.edges())


# g.layout_reingold_tilford(mode="all", root=None, rootlevel=None)

g.layout_grid()
ig.plot(g,"tmp.png")


def github_method():
    G = nx.read_gpickle("divvy.pkl")
    print(list(G.nodes(data=True))[0])
    G_new = G.copy()
    for n1, n2, d in G.edges(data=True):
        if d["count"] < 200:
            G_new.remove_edge(n1, n2)

    g = GeoPlot(
        G_new,
        node_lat="latitude",
        node_lon="longitude",
        node_color="dpcapacity",
        node_size=0.005,
    )
    g.draw()
    plt.show()
if __name__ == '__main__':
    github_method()
