# coding:utf-8
"""
@file: deal_threshold_generationCsv_file.py
@author: wu hao
@time: 2023/8/23 21:23
@env: 封城数据处理
@desc:
@ref:
"""
import os
import time
from math import e, log
import math

import numpy as np
from scipy.spatial import distance
import networkx as nx
import pandas as pd
import csv
import datetime

# from numba import np
from numpy import array
from tqdm import tqdm

#迁徙数据位置
fileNameFront = "F:/百度迁徙数据/比例和指数计算完成后的数据/"


 #判断2个字符串字符是否完全一样 顺序可不同
def compare_two_str(a,b):
    if len(a) != len(b):
        return False
    return sorted(a) == sorted(b)

# 日期时间递增 格式yyyymmdd
def getdaylist(beginDate,endDate):
    beginDate = datetime.datetime.strptime(str(beginDate), "%Y%m%d")
    endDate = datetime.datetime.strptime(str(endDate), "%Y%m%d")
    dayList = []
    while beginDate <= endDate:
        dayList.append(datetime.datetime.strftime(beginDate, "%Y%m%d"))
        beginDate += datetime.timedelta(days=+1)
    return dayList

def select_around_city_data(beginTime,endTime,threshold,file_project):
    """
    属于第一步
    处理直接去掉0.04阈值后in
    :param beginTime:
    :param endTime:
    :return:
    """
    dayList = getdaylist(beginTime,endTime)
    # 循环取每一天的值
    for i in tqdm( range(len(dayList)),desc="第一步合并：进度", total=len(dayList)):
        # 迁入数据
        try:
            moveIn = pd.read_csv(fileNameFront+"in\\"+dayList[i]+".csv")
        except Exception as problem:
            print("error打开迁入（in）有问题：", problem)
            continue
        # 迁出数据
        try:
            moveOut = pd.read_csv(fileNameFront+"out\\" + dayList[i] + ".csv")
        except Exception as problem:
            print("error打开迁出（out）有问题：", problem)
            continue

        # 创建处理完的数据csv
        # 表头
        field_order_move_in = ["city_name", 'city_id_name', 'num']
        # 开始写入整理完的数据csv
        path_file_in = file_project+"/deal_01/in/"
        if not os.path.exists(path_file_in):
            os.makedirs(path_file_in)
        with open(path_file_in + dayList[i] + "_.csv", 'w',encoding="utf-8", newline='') as csvfile:

            writer = csv.DictWriter(csvfile, field_order_move_in)
            writer.writeheader()
            # move_in 每一行
            for row_in in moveIn.itertuples():
                city_name = getattr(row_in, "city_name")
                city_id_name = getattr(row_in, "city_id_name")
                num = getattr(row_in, "num")

                if num >=threshold:
                    row = {"city_name": city_name, "city_id_name": city_id_name, "num": num}
                    writer.writerow(row)
            csvfile.close()

            path_file_out = file_project + "/deal_01/out/"
            if not os.path.exists(path_file_out):
                os.mkdir(path_file_out)
        with open(path_file_out+ dayList[i] + "_.csv", 'w',encoding="utf-8", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, field_order_move_in)
            writer.writeheader()
            # move_in 每一行
            for row_out in moveOut.itertuples():
                city_name = getattr(row_out, "city_name")
                city_id_name = getattr(row_out, "city_id_name")
                num = getattr(row_out, "num")

                if num >= threshold:
                    row = {"city_name": city_name, "city_id_name": city_id_name, "num": num}
                    writer.writerow(row)
            csvfile.close()

def merge_inAndout_file(beginTime,endTime,file_project):
    """
    属于第二步 合并in和out里面的重复内容
    :param beginTime:
    :param endTime:
    :return:
    """
    dayList = getdaylist(beginTime,endTime)
    # 循环取每一天的值
    for i in tqdm(range(len(dayList)),desc="第二步合并：进度",total=len(dayList)):
        # 创建处理完的数据csv
        # 表头
        field_order_move_in = ["city_name", 'city_id_name', 'num']
        # 开始写入整理完的数据csv
        move_in_data = pd.read_csv(file_project+"/deal_01/in/"+dayList[i]+"_.csv")
        move_out_data = pd.read_csv(file_project+"/deal_01/out/"+dayList[i]+"_.csv")
        path_file_in = file_project  + "/deal_02/"
        if not os.path.exists(path_file_in):
            os.makedirs(path_file_in)
        with open(path_file_in+ dayList[i] + "_.csv", 'w',encoding="utf-8", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, field_order_move_in)
            writer.writeheader()
            for row_in in move_in_data.iterrows():
                list_a = []
                city_name_one = row_in[1]["city_name"]
                city_name_two = row_in[1]["city_id_name"]
                value_one = row_in[1]["num"]
                list_a.append(city_name_one)
                list_a.append(city_name_two)
                for row_out in move_out_data.iterrows():
                    list_b = []
                    city_name_three = row_out[1]["city_name"]
                    city_name_four = row_out[1]["city_id_name"]
                    value_two = row_out[1]["num"]
                    list_b.append(city_name_three)
                    list_b.append(city_name_four)

                    if compare_two_str(list_a,list_b):
                        row = {"city_name": city_name_three, "city_id_name": city_name_four,
                               "num": (float(value_one) + float(value_two))/2}
                        writer.writerow(row)
                        break


def merge_alone_file(beginTime,endTime,file_project):
    """
    第三步，合并单独的in里面的内容
    :param beginTime:
    :param endTime:
    :return:
    """
    dayList = getdaylist(beginTime, endTime)
    # 循环取每一天的值
    for i in tqdm(range(len(dayList)), desc="第三步合并：进度", total=len(dayList)):

        # 表头
        field_order_move_in = ["city_name", 'city_id_name', 'num']
        # 开始写入整理完的数据csv
        need_deal_file_one = pd.read_csv(file_project + "/deal_02/" + dayList[i] + "_.csv")
        need_deal_file_two = pd.read_csv(file_project + "/deal_02/" + dayList[i] + "_.csv")
        path_file_in = file_project  + "/deal_03/"
        if not os.path.exists(path_file_in):
            os.makedirs(path_file_in)
        with open(path_file_in + dayList[i] + "_.csv", 'w', encoding="utf-8", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, field_order_move_in)
            writer.writeheader()
            for row_one in need_deal_file_one.iterrows():
                list_a = []
                city_name_one = row_one[1]["city_name"]
                city_name_two = row_one[1]["city_id_name"]
                value_one = row_one[1]["num"]
                list_a.append(city_name_one)
                list_a.append(city_name_two)
                for row_two in need_deal_file_two.iterrows():
                    list_b = []
                    city_name_three = row_two[1]["city_name"]
                    city_name_four = row_two[1]["city_id_name"]
                    value_two = row_two[1]["num"]
                    list_b.append(city_name_three)
                    list_b.append(city_name_four)
                    if compare_two_str(list_a, list_b):
                        valueColThree = (float(value_one) + float(value_two)) / 2
                        row = {"city_name": city_name_one, "city_id_name": city_name_two, "num": valueColThree}
                        writer.writerow(row)
                        break

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
        weight_num = getattr(row, "num")
        G.add_edge(city_name,city_id_name,weight=weight_num)

        # G.add_edges_from([(city_name, city_id_name)])
    return G



# NO (1) 计算平均点连通性
def averagenodeconnectivity(G):
    """
    返回绘制图表的
    X轴：日期
    Y轴：平均点连通性
    """
    listAverageNodeConnectivity = []
    listAverageNodeConnectivity.append((nx.average_node_connectivity(G)))
    return listAverageNodeConnectivity



# NO (2)计算边数量
def edge_number(G):
    """
    返回绘制图表的
    X轴：日期
    Y轴：平均点连通性
    """
    list_edge_number = []

    list_edge_number.append(len(G.edges()))
    # print("边数量： ", list_edge_number)
    return list_edge_number


# NO (3)计算自然连通性
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




# NO  (5)计算 平均最短路径长度
def average_short_length(G):
    S = [G.subgraph(c).copy() for c in nx.connected_components(G)]
    AEC_LastValue =0
    for C in (G.subgraph(c).copy() for c in nx.connected_components(G)):
        AEC_LastValue = AEC_LastValue + nx.average_shortest_path_length(C)
    return AEC_LastValue / len(S)



# (6)NO  计算 代数连通性
def algebraic_connectivity(G):
    algebraic_connectivity_list = []

    algebraic_connectivity_list.append(nx.algebraic_connectivity(G))
    return algebraic_connectivity_list



# NO  (7)计算  连通性损失指标
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


# NO  (8)计算  最大组件大小
def size_of_largest_component(G):
    S = [G.subgraph(c).copy() for c in nx.connected_components(G)]
    return len(S[0])



# NO  (9)计算 连通分量数量
def number_of_connected_components(G):

    list_number_of_connected_components_everyDay = []

    S = [G.subgraph(c).copy() for c in nx.connected_components(G)]
    list_number_of_connected_components_everyDay.append(len(S))
    return list_number_of_connected_components_everyDay



# NO  (10)计算 全局效率
def globalefficiency(G):

    # Y轴数值
    listGlobalEfficiency = []
    listGlobalEfficiency.append(nx.global_efficiency(G))
    return listGlobalEfficiency




# # (4)计算 点连通性
def caculate_node_connectivity(G,source,target ):
    return nx.node_connectivity(G,source,target)

# # (5)计算 边连通性
def caculate_edge_connectivity(G,source,target ):
    return nx.edge_connectivity(G,source,target)






# # (11)计算 Hub Promoted Index
def hub_promoted_index(G, u, v):
  # 获取节点 u 和 v 的邻居节点集合
  neighbors_u = set(G.neighbors(u))
  neighbors_v = set(G.neighbors(v))
  # 计算交集和最小度的大小
  intersection_size = len(neighbors_u & neighbors_v)
  min_degree = min(G.degree(u), G.degree(v))
  # 如果最小度为零，返回零，否则返回交集除以最小度
  if min_degree == 0:
    return 0
  else:
    return float(intersection_size / min_degree)

def CN(G, nodeij):
    node_i = nodeij[0]
    node_j = nodeij[1]
    neigh_i = set(G.neighbors(node_i))
    neigh_j = set(G.neighbors(node_j))
    neigh_ij = neigh_i.intersection(neigh_j)
    num_cn = len(neigh_ij)

    return num_cn


def AA(G, nodeij):
    node_i = nodeij[0]
    node_j = nodeij[1]
    neigh_i = set(G.neighbors(node_i))
    neigh_j = set(G.neighbors(node_j))
    neigh_ij = neigh_i.intersection(neigh_j)
    aa = 0.0
    if len(neigh_ij) > 0:
        for k in neigh_ij:
            degree_k = G.degree(k)
            if degree_k > 1:
                aa = aa + 1 / np.math.log10(degree_k)
    return aa


def RA(G, nodeij):
    node_i = nodeij[0]
    node_j = nodeij[1]
    neigh_i = set(G.neighbors(node_i))
    neigh_j = set(G.neighbors(node_j))
    neigh_ij = neigh_i.intersection(neigh_j)
    ra = 0.0
    if len(neigh_ij) > 0:
        for k in neigh_ij:
            degree_k = G.degree(k)
            if degree_k > 0:
                ra = ra + 1.0 / degree_k
    return ra


def JACC(G, nodeij):
    node_i = nodeij[0]
    node_j = nodeij[1]
    neigh_i = set(G.neighbors(node_i))
    neigh_j = set(G.neighbors(node_j))

    return CN(G, nodeij) / len(neigh_i | neigh_j)


def LHN(G, nodeij):
    node_i = nodeij[0]
    node_j = nodeij[1]
    neigh_i = set(G.neighbors(node_i))
    neigh_j = set(G.neighbors(node_j))

    return CN(G, nodeij) / len(neigh_i) * len(neigh_j)





# 定义一个函数，计算两个节点的 Salton Index
def salton_index(G, u, v):
  # 获取节点 u 和 v 的邻居节点集合
  neighbors_u = set(G.neighbors(u))
  neighbors_v = set(G.neighbors(v))
  # 计算交集和并集的大小
  intersection_size = len(neighbors_u & neighbors_v)
  union_size = len(neighbors_u | neighbors_v)
  # 如果并集为零，返回零，否则返回交集除以并集的平方根
  if union_size == 0:
    return 0
  else:
    return intersection_size / (union_size ** 0.5)



# 定义一个函数，计算两个节点的 Sørensen Index
def sorensen_index(G, u, v):
  # 获取节点 u 和 v 的邻居节点集合
  neighbors_u = set(G.neighbors(u))
  neighbors_v = set(G.neighbors(v))
  # 计算交集和并集的大小
  intersection_size = len(neighbors_u & neighbors_v)
  union_size = len(neighbors_u | neighbors_v)
  # 如果并集为零，返回零，否则返回交集除以并集的一半
  if union_size == 0:
    return 0
  else:
    return intersection_size / (union_size / 2)

# 定义一个函数，计算两个节点的 Hub Depressed Index
def hub_depressed_index(G, u, v):
  # 获取节点 u 和 v 的邻居节点集合
  neighbors_u = set(G.neighbors(u))
  neighbors_v = set(G.neighbors(v))
  # 计算交集和最大度的大小
  intersection_size = len(neighbors_u & neighbors_v)
  max_degree = max(G.degree(u), G.degree(v))
  # 如果最大度为零，返回零，否则返回交集除以最大度
  if max_degree == 0:
    return 0
  else:
    return intersection_size / max_degree


def get_all_indicators(list_time,file_origion):
    """
    生成训练模型的数据集
    :param list_time:
    :param file_origion:
    :return:
    """
    file_order = ["source_city_name","target_city_name","weight",
                  "node_connectivity","edge_connectivity",
                  'hub_promoted_index', "CN", "AA","RA",
                  "JACC", "LHN", "salton_index","sorensen_index","hub_depressed_index","flag"]
    #拿到索引，和前一天的网络相比是否增加或者保留了连边。
    for index,time_alone in enumerate(list_time[:-1]):
        # 标杆数据 判断边是否增加/移除
        G_standard = drawpicture(file_origion +"deal_02/"+time_alone + "_.csv")
        with open(file_origion + "dataset/dataset_"+time_alone+".csv", 'w', encoding="utf-8", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, file_order)
            writer.writeheader()

            #构建网络
            G = drawpicture(file_origion +"deal_02/"+list_time[index+1] + "_.csv")

            for edge_alone in G.edges():
                weight_num = G[edge_alone[0]][edge_alone[1]]['weight']
                #点连通性
                node_connectivity_value = caculate_node_connectivity(G,  edge_alone[0], edge_alone[1])
                #
                edge_connectivity_value = caculate_edge_connectivity(G,  edge_alone[0], edge_alone[1])
                #
                hub_promoted_index_value = hub_promoted_index(G,  edge_alone[0], edge_alone[1])
                #
                CN_value =  CN(G,  [edge_alone[0], edge_alone[1]])
                #
                AA_value = AA(G,  [edge_alone[0], edge_alone[1]])
                #
                RA_value =RA(G,  [edge_alone[0], edge_alone[1]])
                #
                JACC_value =JACC(G,  [edge_alone[0], edge_alone[1]])
                #
                LHN_value =LHN(G,  [edge_alone[0], edge_alone[1]])
                #
                salton_index_value = salton_index(G,  edge_alone[0], edge_alone[1])
                #
                sorensen_index_value = sorensen_index(G,  edge_alone[0], edge_alone[1])
                #
                hub_depressed_index_value = hub_depressed_index(G,  edge_alone[0], edge_alone[1])
                # 标杆数据 判断边是否增加/移除
                #True =保留 1
                #False = 增加 0

                flag_value = G_standard.has_edge(edge_alone[0], edge_alone[1])
                if str(flag_value) =="True":
                    flag_value=1
                elif str(flag_value) =="False":
                    flag_value=0
                row = {"source_city_name": edge_alone[0],
                        "target_city_name": edge_alone[1],
                       "weight":weight_num,
                        "node_connectivity": node_connectivity_value,
                       "edge_connectivity": edge_connectivity_value,
                       "hub_promoted_index": hub_promoted_index_value,
                       "CN": CN_value,
                       "AA": AA_value,
                       "RA": RA_value,
                       "JACC": JACC_value,
                       "LHN": LHN_value,
                       "salton_index": salton_index_value,
                       "sorensen_index": sorensen_index_value,
                        "hub_depressed_index":hub_depressed_index_value,
                       "flag":flag_value}
                writer.writerow(row)








def get_simple_data_indicators(time_alone,file_origion):
    """
    生成单个网络的指标 生成csv文件后去预测
    :param list_time:
    :param file_origion:
    :return:
    """
    file_order = ["source_city_name","target_city_name","weight",
                  "node_connectivity","edge_connectivity",
                  'hub_promoted_index', "CN", "AA","RA",
                  "JACC", "LHN", "salton_index","sorensen_index","hub_depressed_index","flag"]
    #拿到索引，和前一天的网络相比是否增加或者保留了连边。

    # 标杆数据 判断边是否增加/移除
    G_standard = drawpicture(file_origion +"deal_02/"+time_alone + "_.csv")
    with open(file_origion + "dataset/experiment_data/dataset_"+time_alone+".csv", 'w', encoding="utf-8", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, file_order)
        writer.writeheader()

        #构建网络
        G = drawpicture(file_origion +"deal_02/"+time_alone+ "_.csv")

        for edge_alone in G.edges():
            weight_num = G[edge_alone[0]][edge_alone[1]]['weight']
            #点连通性
            node_connectivity_value = caculate_node_connectivity(G,  edge_alone[0], edge_alone[1])
            #
            edge_connectivity_value = caculate_edge_connectivity(G,  edge_alone[0], edge_alone[1])
            #
            hub_promoted_index_value = hub_promoted_index(G,  edge_alone[0], edge_alone[1])
            #
            CN_value =  CN(G,  [edge_alone[0], edge_alone[1]])
            #
            AA_value = AA(G,  [edge_alone[0], edge_alone[1]])
            #
            RA_value =RA(G,  [edge_alone[0], edge_alone[1]])
            #
            JACC_value =JACC(G,  [edge_alone[0], edge_alone[1]])
            #
            LHN_value =LHN(G,  [edge_alone[0], edge_alone[1]])
            #
            salton_index_value = salton_index(G,  edge_alone[0], edge_alone[1])
            #
            sorensen_index_value = sorensen_index(G,  edge_alone[0], edge_alone[1])
            #
            hub_depressed_index_value = hub_depressed_index(G,  edge_alone[0], edge_alone[1])
            # 标杆数据 判断边是否增加/移除
            #True =保留 1
            #False = 增加/移除 0

            flag_value = G_standard.has_edge(edge_alone[0], edge_alone[1])
            if str(flag_value) =="True":
                flag_value=1
            elif str(flag_value) =="False":
                flag_value=0
            row = {"source_city_name": edge_alone[0],
                    "target_city_name": edge_alone[1],
                   "weight":weight_num,
                    "node_connectivity": node_connectivity_value,
                   "edge_connectivity": edge_connectivity_value,
                   "hub_promoted_index": hub_promoted_index_value,
                   "CN": CN_value,
                   "AA": AA_value,
                   "RA": RA_value,
                   "JACC": JACC_value,
                   "LHN": LHN_value,
                   "salton_index": salton_index_value,
                   "sorensen_index": sorensen_index_value,
                    "hub_depressed_index":hub_depressed_index_value,
                   "flag":flag_value}
            writer.writerow(row)



















if __name__ == '__main__':
    # 处理生成大论文第二部分数据集 csv 文件
    listData = ["20210101","20210102","20210103","20210104","20210108","20210109","20210110","20210111","20210112","20210113"]
    file_origion= r"F:/封城数据处理/forecast_traffic_network/data/"
    get_all_indicators(listData, file_origion)
















    #处理源文件网络结构
    # beginTime = 20201201
    # endTime = 20211201
    # threshold = 0.02
    # file_project_one = r"F:/封城数据处理/forecast_traffic_network/data/"
    # select_around_city_data(beginTime, endTime, threshold,file_project_one)
    # merge_inAndout_file(beginTime, endTime,file_project_one)
    # merge_alone_file(beginTime, endTime,file_project_one)





