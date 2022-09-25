#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/25 11:35
# @Author  : wuhao
# @Email   : guess?????
# @File    : find_many_Diff_edge_connect_number.py

import csv

import networkx as nx
import pandas as pd
import collections
# 根据路径画图
def drawpicture(filePath):
    """
    输入文件路径最后绘制成图G
    """
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
def find_city_Counter(edges_add_list):
    list_new_data =[]
    for i in edges_add_list:
        for j in i.split('-'):
            list_new_data.append(j )
    count=collections.Counter(list_new_data)
    #{'武汉': 7, '上海': 7, '合肥': 7,}
    return count
#增加连边计算平均点连通性
def useCity_addEdges_Tocaculate_connect_number(city_name,add_edges,G_contrast):
    """
    使用边列表和城市名 计算增加某一天网络的连边 计算平均点连通性  保留两位小数
    :param city_name: 城市
    :param add_edges: 列表
    :return:
    """
    global S
    for edge_name_want in add_edges:
        if edge_name_want.find(city_name) != -1:
                first_city = edge_name_want[0:edge_name_want.rfind('-', 1)]
                second_city = edge_name_want[edge_name_want.rfind('-', 1) + 1:]
                # print(first_city,second_city)
                G_contrast.add_edges_from([(first_city, second_city)])
                S = [G_contrast.subgraph(c).copy() for c in nx.connected_components(G_contrast)]
    return  len(S)
#减少连边计算平均点连通性
def userCity_removeEdges_Tocaculate_connect_number(city_name,add_edges,G_contrast):
    """
    使用边列表和城市名 计算减少某一天网络的连边 计算平均点连通性  保留两位小数
    :param city_name: 城市
    :param add_edges: 列表
    :return:
    """
    global S
    for edge_name_want in add_edges:
        if edge_name_want.find(city_name) != -1:
                first_city = edge_name_want[0:edge_name_want.rfind('-', 1)]
                second_city = edge_name_want[edge_name_want.rfind('-', 1) + 1:]
                # print(first_city,second_city)
                G_contrast.remove_edges_from([(first_city, second_city)])
                S = [G_contrast.subgraph(c).copy() for c in nx.connected_components(G_contrast)]
    return len(S)

fileNamePath_one = "F:\\01大连民族\\百度迁徙爬取和数据\\百度迁徙数据-final\\03将两个In和Out相同行合并_最终数据\\"
average_node_result_Edges_fileFront = "D:\\04python project\\01-爬虫-爬取百度迁徙数据\\physicalconnecitvity\\indicators\\data\\connect_number\\result\\"
result_filename  = ['0205-0206data_addEdges.cs_finall_indicators.csv', '0205-0206data_removeEdges_finall_indicators.csv', '0207-0208data_addEdges.cs_finall_indicators.csv', '0207-0208data_removeEdges_finall_indicators.csv', '0208-0209data_addEdges.cs_finall_indicators.csv', '0208-0209data_removeEdges_finall_indicators.csv', '0209-0210data_addEdges.cs_finall_indicators.csv', '0209-0210data_removeEdges_finall_indicators.csv', '0210-0211data_addEdges.cs_finall_indicators.csv', '0210-0211data_removeEdges_finall_indicators.csv', '0212-0213data_addEdges.cs_finall_indicators.csv', '0212-0213data_removeEdges_finall_indicators.csv', '0221-0222data_addEdges.cs_finall_indicators.csv', '0221-0222data_removeEdges_finall_indicators.csv', '0223-0224data_addEdges.cs_finall_indicators.csv', '0223-0224data_removeEdges_finall_indicators.csv', '0306-0307data_addEdges.cs_finall_indicators.csv', '0306-0307data_removeEdges_finall_indicators.csv', '0315-0316data_addEdges.cs_finall_indicators.csv', '0315-0316data_removeEdges_finall_indicators.csv']
result_filename_test  = ['0205-0206data_addEdges.cs_finall_indicators.csv', '0205-0206data_removeEdges_finall_indicators.csv']

def tocsv_mutipul_edges(result_filename_test):
    field_order_move_in = ["city_name", "indicator_value", "edgenum","degree"]
    for result_filename_one in result_filename:
        G_contrast = drawpicture(fileNamePath_one + "2020"+result_filename_one[0:4]+"finalData.csv")
        if result_filename_one[14:15] == "a":
            add_edges_data = pd.read_csv(average_node_result_Edges_fileFront+result_filename_one)  #
            edges_add_list = list(add_edges_data["edges"])
            count_add = find_city_Counter(edges_add_list)
            with open(average_node_result_Edges_fileFront +"multiple_cityedge_connectNumber\\" + result_filename_one[0:9]+"addEdgesValue.csv" , 'w', encoding="utf-8", newline='') as csvfile:
                writer = csv.DictWriter(csvfile, field_order_move_in)
                writer.writeheader()
                # dict_cite_value = {}
                for city_name_need_run in count_add.most_common():
                    # print(city_name_need_run[0], city_name_need_run[1])
                    final_value = useCity_addEdges_Tocaculate_connect_number(city_name_need_run[0],edges_add_list,G_contrast)
                    # dict_cite_value[city_name_need_run] = final_value
                    # sorted(dict_cite_value.items(), key=lambda x: x[1], reverse=True)
                    row = {"city_name": city_name_need_run[0], "indicator_value": final_value, "edgenum": city_name_need_run[1],"degree":G_contrast.degree(city_name_need_run)}
                    writer.writerow(row)
            df = pd.read_csv(average_node_result_Edges_fileFront +"multiple_cityedge_connectNumber\\" + result_filename_one[0:9]+"addEdgesValue.csv" )
            df.sort_values(by="indicator_value",ascending=False)
        elif result_filename_one[14:15] == "r":
            remove_edges_data = pd.read_csv(average_node_result_Edges_fileFront + result_filename_one)
            remove_add_list = list(remove_edges_data["edges"])
            count_remove = find_city_Counter(remove_add_list)
            with open(average_node_result_Edges_fileFront +"multiple_cityedge_connectNumber\\" + result_filename_one[0:9]+"removeEdgesValue.csv" , 'w', encoding="utf-8", newline='') as csvfile:
                writer = csv.DictWriter(csvfile, field_order_move_in)
                writer.writeheader()
                # dict_cite_value = {}
                for city_name_need_run in count_remove.most_common():
                    # print(city_name_need_run[0], city_name_need_run[1])
                    final_value = userCity_removeEdges_Tocaculate_connect_number(city_name_need_run[0],remove_add_list,G_contrast)
                    # dict_cite_value[city_name_need_run] = final_value
                    # sorted(dict_cite_value.items(), key=lambda x: x[1], reverse=True)
                    row = {"city_name": city_name_need_run[0], "indicator_value": final_value, "edgenum": city_name_need_run[1],"degree":G_contrast.degree(city_name_need_run)}
                    writer.writerow(row)
            df = pd.read_csv(average_node_result_Edges_fileFront + "multiple_cityedge_connectNumber\\" + result_filename_one[0:9] + "removeEdgesValue.csv")
            df.sort_values(by="indicator_value", ascending=False)
#
# print(list(add_edges_data["edges"]))

#测试
# print(useCity_addEdges_Tocaculate_average_node_connectity("武汉",edges_add_list))  #1.213327825967231    1.1694896304991895, 1.9654004532053313


# {'信阳': '1.22', '武汉': '1.21', '西安': '1.28', '兰州': '1.29', '天水': '1.29', '三门峡': '1.30', '运城': '1.30', '周口': '1.33', '阜阳': '1.33', '商丘': '1.35', '亳州': '1.35', '宿州': '1.36', '郑州': '1.36', '黄冈': '1.39', '九江': '1.39', '榆林': '1.41', '吕梁': '1.41', '焦作': '1.42', '洛阳': '1.42', '葫芦岛': '1.44', '秦皇岛': '1.45', '衢州': '1.46', '上饶': '1.46', '金华': '1.46', '桂林': '1.50', '永州': '1.51', '杭州': '1.52', '上海': '1.52', '菏泽': '1.52', '大理白族自治州': '1.54', '保山': '1.54', '昆明': '1.53', '长沙': '1.53', '宜春': '1.53', '忻州': '1.54', '淮北': '1.54', '大同': '1.56', '乌兰察布': '1.56', '南昌': '1.58', '南充': '1.59', '广元': '1.59', '新乡': '1.59', '开封': '1.60', '曲靖': '1.61', '红河哈尼族彝族自治州': '1.61', '绵阳': '1.61', '遂宁': '1.61', '延安': '1.62', '渭南': '1.62', '赤峰': '1.66', '锡林郭勒盟': '1.66', '遵义': '1.67', '黔南布依族苗族自治州': '1.67', '安顺': '1.67', '铜仁': '1.67', '黔东南苗族侗族自治州': '1.67', '衡阳': '1.68', '株洲': '1.68', '徐州': '1.69', '枣庄': '1.69', '济宁': '1.69', '连云港': '1.70', '日照': '1.71', '岳阳': '1.73', '荆州': '1.73', '湘西土家族苗族自治州': '1.74', '恩施土家族苗族自治州': '1.74', '郴州': '1.74', '张家口': '1.75', '天津': '1.76', '江门': '1.76', '阳江': '1.76', '石家庄': '1.76', '潮州': '1.77', '揭阳': '1.77', '重庆': '1.78', '资阳': '1.78', '巴彦淖尔': '1.78', '乌海': '1.78', '六安': '1.78', '合肥': '1.77', '六盘水': '1.77', '黔西南布依族苗族自治州': '1.77', '内江': '1.77', '保定': '1.78', '茂名': '1.79', '达州': '1.79', '巴中': '1.79', '德州': '1.80', '滨州': '1.80', '滁州': '1.80', '扬州': '1.81', '盐城': '1.81', '蚌埠': '1.81', '无锡': '1.81', '玉林': '1.81', '嘉兴': '1.81', '绍兴': '1.81', '湛江': '1.81', '宿迁': '1.81', '北京': '1.83', '苏州': '1.83', '宣城': '1.83', '南京': '1.83', '漯河': '1.84', '镇江': '1.84', '许昌': '1.84', '青岛': '1.84', '驻马店': '1.84', '泸州': '1.84', '自贡': '1.84', '衡水': '1.85', '邢台': '1.85', '聊城': '1.85', '鞍山': '1.87', '盘锦': '1.87', '清远': '1.88', '东莞': '1.88', '深圳': '1.88', '大连': '1.88', '营口': '1.88', '唐山': '1.88', '廊坊': '1.88', '沧州': '1.88', '常州': '1.89', '泰州': '1.89', '济南': '1.89', '邯郸': '1.89', '西宁': '1.89', '成都': '1.89', '临汾': '1.90', '长治': '1.90', '南通': '1.90', '朝阳': '1.90', '铁岭': '1.91', '四平': '1.91', '潍坊': '1.91', '晋中': '1.91', '南阳': '1.91', '平顶山': '1.91', '东营': '1.92', '娄底': '1.93', '湘潭': '1.93', '龙岩': '1.93', '福州': '1.93', '淄博': '1.93', '三明': '1.93', '南平': '1.93', '泉州': '1.93', '丹东': '1.93', '广州': '1.93', '太原': '1.93', '晋城': '1.93', '珠海': '1.93', '漳州': '1.93', '临沂': '1.93', '益阳': '1.94', '鹤壁': '1.94', '厦门': '1.94', '莆田': '1.94', '佛山': '1.93', '定西': '1.93', '怀化': '1.96', '邵阳': '1.96', '常德': '1.97', '张家界': '1.97', '白城': '1.96', '松原': '1.96', '钦州': '1.96', '防城港': '1.96', '楚雄彝族自治州': '1.96', '贵阳': '1.96', '鄂州': '1.96', '广安': '1.96', '齐齐哈尔': '1.96', '黑河': '1.96', '朔州': '1.96', '景德镇': '1.96', '淮南': '1.96', '韶关': '1.96', '昭通': '1.96', '宜昌': '1.96', '芜湖': '1.96', '潜江': '1.96', '萍乡': '1.96', '通辽': '1.97', '沈阳': '1.97', '鹰潭': '1.97', '天门': '1.97', '新余': '1.97', '梧州': '1.99', '池州': '1.99', '贺州': '1.99', '铜陵': '1.99', '佳木斯': '1.98', '鹤岗': '1.98', '辽源': '1.97', '长春': '1.97', '南宁': '1.97', '临沧': '1.97', '兴安盟': '1.97', '济源': '1.97', '白山': '1.97', '安庆': '1.97', '西双版纳傣族自治州': '1.97', '贵港': '1.97', '平凉': '1.97', '陇南': '1.97'}

tocsv_mutipul_edges(result_filename)