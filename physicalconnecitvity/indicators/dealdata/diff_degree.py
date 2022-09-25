#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/2 14:17
# @Author  : wuhao
# @Email   : guess?????
# @File    : diff_degree.py

import csv
import os

import networkx as nx
import pandas as pd
import collections
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
        city_name = getattr(row, "city_name")
        city_id_name = getattr(row, "city_id_name")
        G.add_edges_from([(city_name, city_id_name)])
    return G
#寻找城市的连边数量 返回Counter()
#寻找城市的连边数量 返回Counter()
def find_city_Counter(edges_add_list,first_name,second_name):
    list_new_data =[]
    for row in edges_add_list.iterrows():
        list_new_data.append(row[1][first_name])
        list_new_data.append(row[1][second_name])
    count=collections.Counter(list_new_data)
    #{'武汉': 7, '上海': 7, '合肥': 7,}
    return count
#增加连边计算平均点连通性
def useCity_addEdges_Tocaculate_connect_number(city_name,add_edges,G_contrast,first_name,second_name):
    """
    使用边列表和城市名 计算增加某一天网络的连边 计算平均点连通性  保留两位小数
    :param city_name: 城市
    :param add_edges: 列表
    :return:
    """
    global S
    for row in add_edges.iterrows():
        if row[1][first_name] == city_name or row[1][second_name] ==  city_name:
            # print(first_city,second_city)
            G_contrast.add_edges_from([(row[1][first_name], row[1][second_name])])
    return  G_contrast.degree(city_name)
#减少连边计算平均点连通性
def userCity_removeEdges_Tocaculate_connect_number(city_name,add_edges,G_contrast,first_name,second_name):
    """
    使用边列表和城市名 计算减少某一天网络的连边 计算平均点连通性  保留两位小数
    :param city_name: 城市
    :param add_edges: 列表
    :return:
    """
    global S
    for row in add_edges.iterrows():
        if row[1][first_name] == city_name or row[1][second_name] == city_name:
            # print(first_city,second_city)
            G_contrast.remove_edges_from([(row[1][first_name], row[1][second_name])])
    return G_contrast.degree(city_name)

fileNamePath_one = "F:\\01大连民族\\百度迁徙爬取和数据\\百度迁徙数据-final\\03将两个In和Out相同行合并_最终数据\\"
Edges_fileFront = "D:\\04python project\\01-爬虫-爬取百度迁徙数据\\physicalconnecitvity\\indicators\\data\\finall_data\\"
result_filename  = os.listdir(Edges_fileFront)
print(result_filename)
result_filename_test  = ['0205-0206data_addEdges.cs_finall_indicators.csv', '0205-0206data_removeEdges_finall_indicators.csv']

def tocsv_mutipul_edges(result_filename):
    first_name_remove = "city_name_remove"
    second_name_remove = "city_id_name_remove"
    first_name_add = "city_name_add"
    second_name_add = "city_id_name_add"
    field_order_move_in = ["city_name", "degree_superNode","degree_origion" ,"edgenum"]
    for result_filename_one in result_filename:
        G_contrast = drawpicture(fileNamePath_one + "2020"+result_filename_one[0:4]+"finalData.csv")

        if result_filename_one[14:15] == "a":
            add_edges_data = pd.read_csv(Edges_fileFront+result_filename_one)  #
            count_add = find_city_Counter(add_edges_data,first_name_add,second_name_add)
            with open(Edges_fileFront +"diff_degree\\" + result_filename_one[0:9]+"addEdgesValue.csv" , 'w', encoding="utf-8", newline='') as csvfile:
                writer = csv.DictWriter(csvfile, field_order_move_in)
                writer.writeheader()
                # dict_cite_value = {}
                for city_name_need_run in count_add.most_common():
                    degree_origion = G_contrast.degree(city_name_need_run[0])
                    final_value_degree_add = useCity_addEdges_Tocaculate_connect_number(city_name_need_run[0],add_edges_data,G_contrast,first_name_add,second_name_add)
                    # dict_cite_value[city_name_need_run] = final_value
                    # sorted(dict_cite_value.items(), key=lambda x: x[1], reverse=True)
                    row = {"city_name": city_name_need_run[0], "degree_superNode": final_value_degree_add, "degree_origion":degree_origion , "edgenum": city_name_need_run[1]}
                    writer.writerow(row)
            df = pd.read_csv(Edges_fileFront +"diff_degree\\" + result_filename_one[0:9]+"addEdgesValue.csv" )
            df.sort_values(by="degree_origion",ascending=False)
        elif result_filename_one[14:15] == "r":
            remove_edges_data = pd.read_csv(Edges_fileFront + result_filename_one)
            count_remove = find_city_Counter(remove_edges_data,first_name_remove,second_name_remove)
            with open(Edges_fileFront +"diff_degree\\" + result_filename_one[0:9]+"removeEdgesValue.csv" , 'w', encoding="utf-8", newline='') as csvfile:
                writer = csv.DictWriter(csvfile, field_order_move_in)
                writer.writeheader()
                # dict_cite_value = {}
                for city_name_need_run in count_remove.most_common():
                    degree_origion = G_contrast.degree(city_name_need_run[0])
                    final_value_degree_remove = userCity_removeEdges_Tocaculate_connect_number(city_name_need_run[0],remove_edges_data,G_contrast,first_name_remove,second_name_remove)
                    # dict_cite_value[city_name_need_run] = final_value
                    # sorted(dict_cite_value.items(), key=lambda x: x[1], reverse=True)
                    row = {"city_name": city_name_need_run[0], "degree_superNode": final_value_degree_remove, "degree_origion":degree_origion, "edgenum": city_name_need_run[1]}
                    writer.writerow(row)
            df = pd.read_csv(Edges_fileFront + "diff_degree\\" + result_filename_one[0:9] + "removeEdgesValue.csv")
            df.sort_values(by="degree_origion", ascending=False)

#测试
tocsv_mutipul_edges(result_filename)




