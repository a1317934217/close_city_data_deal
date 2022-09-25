#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/9 11:27
# @Author  : wuhao
# @Email   : guess?????
# @File    : creat_node_Js.py
import os
# 根据路径画图
import networkx as nx
import pandas as pd

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
def deal_graph(edges_add_list,first_name,second_name,G_graph,sign):
    """
    处理图 增加边或者删除边
    :param edges_add_list:
    :param first_name:
    :param second_name:
    :param G_graph:
    :param sign:
    :return:
    """
    if sign == "a":
        for row in edges_add_list.iterrows():
            G_graph.add_edges_from([(row[1][first_name], row[1][second_name])])
    elif sign =="r":
        for row in edges_add_list.iterrows():
            G_graph.remove_edges_from([(row[1][first_name], row[1][second_name])])
    return G_graph

def deal_graph_simple(edges_add_list,first_name,second_name):
    """

    :param edges_add_list:
    :param first_name:
    :param second_name:
    :param sign:
    :return:
    """
    G = nx.Graph()
    for row in edges_add_list.iterrows():
        G.add_edges_from([(row[1][first_name], row[1][second_name])])
    return G

fileNamePath_one = "F:\\01大连民族\\百度迁徙爬取和数据\\百度迁徙数据-final\\03将两个In和Out相同行合并_最终数据\\"
Edges_fileFront = "D:\\04python project\\01-爬虫-爬取百度迁徙数据\\physicalconnecitvity\\indicators\\data\\finall_data\\"
edge_js_name = "D:\\04python project\\01-爬虫-爬取百度迁徙数据\\physicalconnecitvity\\mapvisualization\\edge\\"
node_js_name = "D:\\04python project\\01-爬虫-爬取百度迁徙数据\\physicalconnecitvity\\mapvisualization\\node\\"
result_filename = os.listdir(Edges_fileFront)
result_filename.pop()
print(result_filename)

def to_js_edge_file(G_mode,js_filename_path):
    """
    抽取生成边的js方法 用来可视化
    :param G_mode:
    :param js_filename_path:
    :return:
    """
    list_finall_data_edge_origion=[]
    for row in G_mode.edges():
        list_need_append = []
        dict_need_one = {}
        dict_need_two = {}
        first_city = row[0]
        second_city = row[1]
        dict_need_one["name"] = first_city
        dict_need_two["name"] = second_city
        list_need_append.append(dict_need_one)
        list_need_append.append(dict_need_two)
        list_finall_data_edge_origion.append(list_need_append)
    with open(js_filename_path, 'w', encoding='UTF-8') as f:
        f.write("var edges = " + str(list_finall_data_edge_origion))
        f.close()
def to_js_node_file(G_mode,js_filename_path):
    """
    抽取生成点的js方法 用来可视化
    :param G_mode:
    :param js_filename_path:
    :return:
    """
    list_finall_data_node=[]
    for row_node in G_mode.nodes():
        list_need_append = []
        dict_need_one = {}
        dict_need_one["name"] = row_node
        list_need_append.append(dict_need_one)
        list_finall_data_node.append(list_need_append)
    with open(js_filename_path, 'w', encoding='UTF-8') as f_origion:
        f_origion.write("var nodes = " + str(list_finall_data_node))
        f_origion.close()


def to_node_and_edge_js(result_filename):
    """
    生成增加点或者边的全部 all
    :param result_filename:
    :return:
    """
    first_name_remove = "city_name_remove"
    second_name_remove = "city_id_name_remove"
    first_name_add = "city_name_add"
    second_name_add = "city_id_name_add"
    for result_filename_one in result_filename:
        G_contrast = drawpicture(fileNamePath_one + "2020"+result_filename_one[0:4]+"finalData.csv")
        G_contrast_last = drawpicture(fileNamePath_one + "2020"+result_filename_one[5:9]+"finalData.csv")

        to_js_edge_file(G_contrast,edge_js_name+"2020"+result_filename_one[0:4]+".js")
        to_js_edge_file(G_contrast_last,edge_js_name+"2020"+result_filename_one[5:9]+".js")
        to_js_node_file(G_contrast,node_js_name+"2020"+result_filename_one[0:4]+".js")
        to_js_node_file(G_contrast_last,node_js_name+"2020"+result_filename_one[5:9]+".js")

        language_file_name_remove_edge = 'remove_Edges.js'
        language_file_name_remove_node = 'remove_Node.js'
        language_file_name_add_edge = 'add_Edges.js'
        language_file_name_add_node = 'add_Node.js'
        if result_filename_one[14:15] == "a":
            add_edges_data = pd.read_csv(Edges_fileFront+result_filename_one)  #
            G_graph_add = deal_graph(add_edges_data,first_name_add,second_name_add,G_contrast,"a")

            to_js_edge_file(G_graph_add,edge_js_name+result_filename_one[0:9] + language_file_name_add_edge)
            to_js_node_file(G_graph_add,node_js_name+result_filename_one[0:9] + language_file_name_add_node)
        elif result_filename_one[14:15] == "r":

            remove_edges_data = pd.read_csv(Edges_fileFront + result_filename_one)
            G_graph_remove = deal_graph(remove_edges_data, first_name_remove, second_name_remove, G_contrast, "r")

            to_js_edge_file(G_graph_remove, edge_js_name + result_filename_one[0:9] + language_file_name_remove_edge)
            to_js_node_file(G_graph_remove, node_js_name + result_filename_one[0:9] + language_file_name_remove_node)

def to_js_node_edge_simple(js_filename_path):
    """
    生成 只有边或者点的js文件
    :param js_filename_path:
    :return:
    """
    first_name_remove = "city_name_remove"
    second_name_remove = "city_id_name_remove"
    first_name_add = "city_name_add"
    second_name_add = "city_id_name_add"

    for result_filename_one in js_filename_path:
        if result_filename_one[14:15] == "a":
            add_edges_data = pd.read_csv(Edges_fileFront+result_filename_one)
            G_add = deal_graph_simple(add_edges_data,first_name_add,second_name_add)
            to_js_edge_file(G_add,edge_js_name+"edge_new_simple\\"+result_filename_one[0:9]+"only_addEdges.js")
            to_js_node_file(G_add,node_js_name+"node_new_simple\\"+result_filename_one[0:9]+"only_addnode.js")
        elif result_filename_one[14:15] == "r":
            remove_edges_data = pd.read_csv(Edges_fileFront + result_filename_one)
            G_remove = deal_graph_simple(remove_edges_data, first_name_remove, second_name_remove)
            to_js_edge_file(G_remove, edge_js_name + "edge_new_simple\\"+result_filename_one[0:9] + "only_removeEdges.js")
            to_js_node_file(G_remove, node_js_name + "node_new_simple\\"+result_filename_one[0:9] + "only_removenode.js")

#测试
# to_node_and_edge_js(resul t_filename)

to_js_node_edge_simple(result_filename)


# G_day_one = pd.read_csv(Edges_fileFront+"0101-0102data_addEdges.csv")
# for row_node in G_day_one.iterrows():
#     print(row_node[1]["city_name_add"])
# S = [G_day_one.subgraph(c).copy() for c in nx.connected_components(G_day_one)]
# print("连通分量：", len(S))
# for i in S:
#     print(i)
# Graph with 287 nodes and 758 edges
