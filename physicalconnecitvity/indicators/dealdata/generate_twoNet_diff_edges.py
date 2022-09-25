#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/8 11:01
# @Author  : wuhao
# @Email   : guess?????
# @File    : extractNodeEdge.py
import pandas as pd
import networkx as nx
from matplotlib import pyplot as plt

#冒泡
from pandas import DataFrame


def bubbleSort(arr):
    n = len(arr)
    # 遍历所有数组元素
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            if arr[j][2]["weight"] < arr[j + 1][2]["weight"]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
#元组比较
def compare_twoTuple(tuple_one,tuple_two):
    set_one = {tuple_one[0],tuple_one[1]}
    set_two = {tuple_two[0],tuple_two[1]}
    if set_one == set_two:
        return True
#找最大列表
def max_list(first,second):
    if len(first) >= len(second):
        return first,second
    else:
        return second,first
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
        # edge_weight = getattr(row, "num")
        # hang = []
        # # 添加节点 两个 是有向的
        # hang.append(city_name)
        # hang.append(city_id_name)
        # # 添加边的信息
        # weight = {}
        # weight["weight"] = edge_weight
        # hang.append(weight)
        # edge_data_info.append(hang)
        G.add_edges_from([(city_name, city_id_name)])
        # G.add_weighted_edges_from([(city_name, city_id_name, weight["weight"]=)
    # G.add_edges_from(edge_data_info)
    return G
def  find_diff_edges_of_AandB(llist1,list2):
    # 列表b中包含而列表A中没有的元素
    differ_list_b = list(set(list2).difference(set(llist1)))
    # 列表a中包含而列表b中没有的元素
    differ_list_a = list(set(llist1).difference(set(list2)))
    #深拷贝复制
    deepCopy_G_a = differ_list_a[:]
    deepCopy_G_b = differ_list_b[:]
    for i in range(len(differ_list_a)):
        for j in range(len(differ_list_b)):
            if compare_twoTuple(differ_list_a[i], differ_list_b[j]):
                deepCopy_G_a.remove(differ_list_a[i])
                deepCopy_G_b.remove(differ_list_b[j])
    return deepCopy_G_a,deepCopy_G_b



lista_all = ["0319"]
listb_all = ["0320"]
filepath_front ="D:\\04python project\\01-爬虫-爬取百度迁徙数据\\physicalconnecitvity\\indicators\\data\\finall_data\\"
for first_data,second_data in zip(lista_all,listb_all):
    fileNamePath_one = "F:\\01大连民族\\百度迁徙爬取和数据\\百度迁徙数据-final\\" \
                       "03将两个In和Out相同行合并_最终数据\\2020"+first_data+"finalData.csv"
    fileNamePath_two = "F:\\01大连民族\\百度迁徙爬取和数据\\百度迁徙数据-final\\" \
                       "03将两个In和Out相同行合并_最终数据\\2020"+second_data+"finalData.csv"
    file_name_end_removeEdges = first_data+"-"+second_data+"data_removeEdges.csv"
    file_name_end_addEdges = first_data+"-"+second_data+"data_addEdges.csv"

    Gdemo_one = drawpicture(fileNamePath_one)
    print(first_data+"的边：",len(Gdemo_one.edges()),len(Gdemo_one.nodes()))
    Gdemo_two = drawpicture(fileNamePath_two)
    print(second_data + "的边：", len(Gdemo_two.edges()), len(Gdemo_two.nodes()))
    # print(Gdemo_one)
    alledges_one = list(Gdemo_one.edges())
    alledges_two = list(Gdemo_two.edges())
    A_have_B_no, B_have_A_no = find_diff_edges_of_AandB(alledges_one, alledges_two)

    order1 = ['city_name_remove', 'city_id_name_remove']
    order2 = ['city_name_add', 'city_id_name_add']
    df1 = DataFrame(data=A_have_B_no, columns=order1)
    df2 = DataFrame(data=B_have_A_no, columns=order2)
    df1.to_csv(filepath_front+file_name_end_removeEdges, index=False, encoding="utf-8-sig")
    df2.to_csv(filepath_front+file_name_end_addEdges, index=False, encoding="utf-8-sig")




# alledges_one = [('苏州', '宿迁'), ('梧州', '贵港'), ('苏州', '镇江'),("bvnkjks",'giuiegr')]
# alledges_two = [('苏州', '宿迁'), ('贵港', '梧州'), ('镇江', '苏州'),('awdaw','awddff')]
#
# fileNamePath_one = "F:\\01大连民族\\百度迁徙爬取和数据\\百度迁徙数据-final\\" \
#                    "03将两个In和Out相同行合并_最终数据\\20200212finalData.csv"
# fileNamePath_two = "F:\\01大连民族\\百度迁徙爬取和数据\\百度迁徙数据-final\\" \
#                    "03将两个In和Out相同行合并_最终数据\\20200213finalData.csv"
#
#
# Gdemo_one = drawpicture(fileNamePath_one)
# Gdemo_two = drawpicture(fileNamePath_two)
# # print(Gdemo_one)
# alledges_one = list(Gdemo_one.edges())
# alledges_two = list(Gdemo_two.edges())
# A_have_B_no, B_have_A_no = find_diff_edges_of_AandB(alledges_one, alledges_two)
# print(A_have_B_no, B_have_A_no )
#
#
#
#
#














# A_have_B_no, B_have_A_no = find_diff_edges_of_AandB(alledges_one, alledges_two)
# print(A_have_B_no, B_have_A_no)
# cccc=[]
# cccc.append(A_have_B_no)
# cccc.append(B_have_A_no)
# #最后排序的结果
# lastvalue = bubbleSort(deepCopy_G)
# order1 = ['city_name_remove', 'city_id_name_remove']
# order2 = ['city_name_add', 'city_id_name_add']
#
# df1=DataFrame(data =A_have_B_no,columns=order1)
# print(df1)
# df2=DataFrame(data =B_have_A_no,columns=order2)
#
# test = pd.concat([df1, df2])
# print(test)
# #输出为csv
# test.to_csv('D:\\04python project\\01-爬虫-爬取百度迁徙数据\\'
# 'physicalconnecitvity\indicators\\data\\adadad.csv', index=False, encoding="utf-8-sig")

# maxG = [('苏州', '宿迁'), ('梧州', '贵港'), ('苏州', '镇江')]
# minG = [('苏州', '宿迁'), ('贵港', '梧州'), ('镇江', '苏州'),('awdaw','awddff')]









# Gra = nx.Graph()
# Gra.add_edges_from(S[10].edges())
# pos = nx.spring_layout(Gdemo_one)
# nx.draw(Gdemo_one, pos, node_size=20, node_color="red", edge_color="black", width=0.5)
# plt.show()
#
# pos = nx.spring_layout(Gdemo_two)
# nx.draw(Gdemo_two, pos, node_size=20, node_color="red", edge_color="black", width=0.5)
# plt.show()



# print("平均聚类稀系数Gdemo_one：", nx.average_clustering(Gdemo_one))
# print("平均聚类稀系数Gdemo_two：", nx.average_clustering(Gdemo_two))
#
# print("点数量Gdemo_one：", nx.number_of_nodes(Gdemo_one))
# print("点数量Gdemo_two：", nx.number_of_nodes(Gdemo_two))
#
# print("边数量Gdemo_one：", nx.number_of_edges(Gdemo_one))
# print("边数量Gdemo_two：", nx.number_of_edges(Gdemo_two))

# print("图密度Gdemo_one：", nx.density(Gdemo_one))
# print("图密度Gdemo_two：", nx.density(Gdemo_two))
#
#
#
# average_degree_one =0
# for i in Gdemo_one.degree():
#     average_degree_one += int(i[1])
# print("平均度 Gdemo_one：", average_degree_one/nx.number_of_nodes(Gdemo_one))
#
#
# average_degree_two =0
# for i in Gdemo_two.degree():
#     average_degree_two += int(i[1])
# print("平均度 Gdemo_two：", average_degree_two/nx.number_of_nodes(Gdemo_two))
#
#
# S_one = [Gdemo_one.subgraph(c).copy() for c in nx.connected_components(Gdemo_one)]
# S_two = [Gdemo_two.subgraph(c).copy() for c in nx.connected_components(Gdemo_two)]
# print("连通分量数量Gdemo_one：", len(S_one))
# print("连通分量数量Gdemo_two：", len(S_two))



# print("度分布序列Gdemo_one：",nx.degree_histogram(Gdemo_one))
# print("度分布序列Gde                                                                                                                                      mo_two：", nx.degree_histogram(Gdemo_two))


