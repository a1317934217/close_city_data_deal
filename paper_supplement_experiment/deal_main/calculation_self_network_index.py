# coding:utf-8
"""
@file: close_city_caculate_indicator.py
@author: wu hao
@time: 2022/9/27 7:53
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
#处理后存储的位置
file_project =  r"F:/封城数据处理/paper_supplement_experiment/data/"

beijing_one_network = ["北京","廊坊","天津","保定","张家口","唐山","石家庄","上海","承德","沧州","邯郸"]
hengshui_one_network = ["衡水","石家庄","北京","保定","沧州","德州","天津","张家口","唐山","邢台","廊坊"]
qinhuangdao_one_network = ["秦皇岛","唐山","北京","天津","葫芦岛","石家庄","廊坊","承德","保定","沧州","张家口"]
tangshan_one_network = ["唐山","北京","天津","秦皇岛","廊坊","石家庄","承德","保定","沧州","张家口","邯郸"]
langfang_one_network = ["廊坊","北京","天津","保定","沧州","石家庄","唐山","衡水","张家口","秦皇岛","承德"]
tianjin_one_network = ["天津","北京","廊坊","沧州","唐山","保定","邯郸","石家庄","张家口","秦皇岛","德州"]
chengde_one_network = ["承德","北京","廊坊","石家庄","唐山","赤峰","天津","保定","秦皇岛","张家口","朝阳"]
baoding_one_network = ["保定","北京","廊坊","石家庄","天津","衡水","沧州","张家口","邯郸","唐山","邢台"]
cangzhou_one_network = ["沧州","北京","天津","保定","石家庄","廊坊","衡水","德州","唐山","滨州","邯郸"]
handan_one_network = ["邯郸","北京","石家庄","邢台","天津","安阳","保定","廊坊","衡水","聊城","濮阳"]
xingtai_one_network = ["邢台","北京","石家庄","邯郸","保定","天津","衡水","聊城","廊坊","沧州","济南"]
zhangjiakou_one_network = ["张家口","石家庄","北京","保定","天津","廊坊","大同","锡林郭勒盟","乌兰察布","济南"]

list_cityName =[beijing_one_network,hengshui_one_network,qinhuangdao_one_network,tangshan_one_network,langfang_one_network,tianjin_one_network,
                chengde_one_network,baoding_one_network,cangzhou_one_network,handan_one_network,xingtai_one_network,zhangjiakou_one_network]





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
def drawpicture(filePath,nodes_list_one):
    """
    输入文件路径最后绘制成图G
    """
    global dataMiga
    G = nx.Graph()
    G.add_nodes_from(nodes_list_one)
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



# 计算平均点连通性
def averagenodeconnectivity(file_path,city_name,nodes):
    """
    返回绘制图表的
    X轴：日期
    Y轴：平均点连通性
    """

    listAverageNodeConnectivity = []
    for i in tqdm (range(len(listXData)),desc="平均点连通性进度",total=len(listXData)):
        # 循环画图
        try:
            filePathInMethon = file_path + listXData[i] +"_"+city_name+".csv"
            G = drawpicture(filePathInMethon,nodes)

        except Exception as problem:
            print("((平均点连通性) error打开迁徙文件出问题：", problem)
        else:
                listAverageNodeConnectivity.append((nx.average_node_connectivity(G)))
    # print("平均点连通性： ", listAverageNodeConnectivity)
    return listAverageNodeConnectivity


# 计算城市度
def get_city_degree(file_path,city_name,nodes):
    """
    返回绘制图表的
    X轴：日期
    Y轴：平均点连通性
    """
    list_city_degree = []
    for i in range(len(listXData)):
        # 循环画图
        try:
            filePathInMethon = file_path + listXData[i] +"_"+city_name+".csv"
            G = drawpicture(filePathInMethon,nodes)

        except Exception as problem:
            print("((城市度) error打开迁徙文件出问题：", problem)
        else:
            list_city_degree.append(len(G.edges(city_name)))
    # print("城市度： ", list_city_degree)
    return list_city_degree


# 计算边数量
def edge_number(file_path,city_name,nodes):
    """
    返回绘制图表的
    X轴：日期
    Y轴：平均点连通性
    """
    list_edge_number = []
    for i in range(len(listXData)):
        # 循环画图
        try:
            filePathInMethon = file_path + listXData[i] +"_"+city_name+".csv"
            G = drawpicture(filePathInMethon,nodes)
        except Exception as problem:
            print("((边数量) error打开迁徙文件出问题：", problem)
        else:
            list_edge_number.append(len(G.edges()))
    # print("边数量： ", list_edge_number)
    return list_edge_number


# 计算自然连通性
def naturecconnectivity(file_path,city_name,nodes_list):
    """
    返回绘制图表的
    X轴：日期
    Y轴：自然连通度数值
    """
    # 时间列表
    listAlgebraicConnectivity = []
    for i in range(len(listXData)):
        # 循环画图
        try:
            filePathInMethon = file_path + listXData[i] +"_"+city_name+".csv"

        except Exception as problem:
            print("(自然连通度) error打开迁徙文件出问题：", problem)
        else:
            G = drawpicture(filePathInMethon,nodes_list)
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
            listAlgebraicConnectivity.append(algebraicConnectivityValue)
    # print("自然连通度： ", listAlgebraicConnectivity)
    return listAlgebraicConnectivity



# 计算  点连通性(单个点)
def node_connectivity_alone(file_path,city_name,nodes):
    """
    返回绘制图表的
    X轴：日期
    Y轴：平均点连通性
    """

    listAverageNodeConnectivity = []
    for i in tqdm (range(len(listXData)),desc="点连通性（单个）进度",total=len(listXData)):
        # 循环画图
        try:
            filePathInMethon = file_path + listXData[i] +"_"+city_name+".csv"
            G = drawpicture(filePathInMethon,nodes)

        except Exception as problem:
            print("点连通性（单独） error打开迁徙文件出问题：", problem)
        else:
                listAverageNodeConnectivity.append((nx.node_connectivity(G,s="石家庄",t="唐山")))
    # print("点连通性（单独）： ", listAverageNodeConnectivity)


# 计算 平均度
def average_degree_alone(file_path,city_name,nodes):
    listAverage_degree = []
    for i in tqdm(range(len(listXData)), desc="平均度 进度", total=len(listXData)):
        # 循环画图
        try:
            filePathInMethon = file_path + listXData[i] + "_" + city_name + ".csv"
            G = drawpicture(filePathInMethon, nodes)

        except Exception as problem:
            print("平均度   error打开迁徙文件出问题：", problem)
        else:
            d = dict(nx.degree(G))
            listAverage_degree.append(sum(d.values()) / len(G.nodes))

    # print("平均度",listAverage_degree)



# 计算 平均最短路径长度
def average_short_length(file_path,city_name,nodes):
    average_short_length_list = []
    for i in tqdm(range(len(listXData)), desc="平均最短路径长度 进度", total=len(listXData)):
        # 循环画图
        try:
            filePathInMethon = file_path + listXData[i] + "_" + city_name + ".csv"
            G = drawpicture(filePathInMethon, nodes)

        except Exception as problem:
            print("平均最短路径长度   error打开迁徙文件出问题：", problem)
        else:
            S = [G.subgraph(c).copy() for c in nx.connected_components(G)]

            AEC_LastValue =0
            for C in (G.subgraph(c).copy() for c in nx.connected_components(G)):
                AEC_LastValue = AEC_LastValue + nx.average_shortest_path_length(C)

            average_short_length_list.append(AEC_LastValue/len(S))
    print("平均最短路径长度",average_short_length_list)



# 计算 代数连通性
def algebraic_connectivity(file_path,city_name,nodes):
    algebraic_connectivity_list = []
    for i in tqdm(range(len(listXData)), desc="代数连通性 进度", total=len(listXData)):
        # 循环画图
        try:
            filePathInMethon = file_path + listXData[i] + "_" + city_name + ".csv"
            G = drawpicture(filePathInMethon, nodes)

        except Exception as problem:
            print("代数连通性   error打开迁徙文件出问题：", problem)
        else:

            algebraic_connectivity_list.append(nx.algebraic_connectivity(G))

    print("代数连通性",algebraic_connectivity_list)














def function_encapsulation(first_data,second_data,third_data,four_data,listXData,ax1,title_name):

    def format_fn(tick_val, tick_pos):
        if int(tick_val) in range(len(listXData)):
            return str(listXData[int(tick_val)])[4:8]
        else:
            return ''
    ax1.xaxis.set_major_formatter(FuncFormatter(format_fn))
    ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
    # plt.ylim((-5, 40))
    # 横坐标每个值旋转90度
    # plt.xticks(rotation=90)

    # 坐标轴ticks的字体大小
    ax1.set_xlabel('日期', fontsize=14)  # 为x轴添加标签
    ax1.set_ylabel('数值', fontsize=14)  # 为y轴添加标签  数值
    ax1.legend()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # 根据需要设置最大最小值，这里设置最大值为1.最小值为0
    # 数据归一化
    tool = MinMaxScaler(feature_range=(0, 1))

    first_data = tool.fit_transform(array(first_data).reshape(-1,1)).tolist()
    second_data = tool.fit_transform(array(second_data).reshape(-1,1)).tolist()
    third_data = tool.fit_transform(array(third_data).reshape(-1,1)).tolist()
    four_data = tool.fit_transform(array(four_data).reshape(-1,1)).tolist()

    plt.title(title_name,fontsize=14)

    # plt.xticks(fontsize=20)
    # plt.yticks(fontsize=20)

    plt.plot(listXData, first_data,  linewidth=1.5,  label='平均点连通性') #"4-",
    plt.plot(listXData, second_data, linewidth=1.5,  label='度')#, "1--"
    plt.plot(listXData, third_data, linewidth=1.5,  label='边数量')#, "1--"
    plt.plot(listXData, four_data, linewidth=1.5,  label='自然连通性')#, "1--"



    plt.scatter(6, 1, s=50, color='cyan')
    plt.plot([6, 6], [1, 0], 'x--', lw=1.5)
    plt.text(0, 0.90, r'封城开始', fontdict={'size': '14', 'color': 'black'})

    plt.scatter(28, 1, s=50, color='cyan')
    plt.plot([28, 28], [1, 0], 'x--', lw=1.5)
    plt.text(27, 0.90, r'封城结束', fontdict={'size': '14', 'color': 'black'})
    plt.legend()

    plt.scatter(92, 1, s=50, color='cyan')
    plt.plot([92, 92], [1, 0], 'x--', lw=1.5)
    plt.text(91, 0.90, r'清明节', fontdict={'size': '14', 'color': 'black'})

    plt.scatter(120, 1, s=50, color='cyan')
    plt.plot([120, 120], [1, 0], 'x--', lw=1.5)
    plt.text(119, 0.90, r'劳动节', fontdict={'size': '14', 'color': 'black'})







def draw_all_city_indicators(beginData,endData):
    listXData = getdaylist(beginData, endData)
    fig = plt.figure(figsize=(8, 6), dpi=300)

    final_file_adress = "F:/封城数据处理/paper_supplement_experiment/data/all_city_indicators.csv"
    move_data = pd.read_csv(final_file_adress, encoding="utf-8")
    i=1
    for move_data in move_data.iterrows():
        city_name  = move_data[1]['city_name']
        list_avarge_node  = list(move_data[1]['list_avarge_node'][1:-1].split(","))
        list_degree  = list(move_data[1]['list_degree'][1:-1].split(","))
        list_edge  = list(move_data[1]['list_edge'][1:-1].split(","))
        list_nature  = list(move_data[1]['list_nature'][1:-1].split(","))
        ax = fig.add_subplot(4,3,i)

        # print(type(value_in))
        # print((value_in))
        # print(type(value_out))
        function_encapsulation(list(map(float, list_avarge_node)), list(map(float, list_degree)),
                               list(map(float, list_edge)), list(map(float, list_nature)) ,
        listXData,ax, city_name)
        i+=1

    plt.show()


def caculate_indicators():
    around_city = ["北京", "衡水", "秦皇岛", "唐山", "廊坊", "天津", "承德", "保定", "沧州", "邯郸", "邢台", "张家口"]
    # 表头
    field_order_move_in = ["city_name", 'level', 'list_avarge_node', 'list_degree', 'list_edge', 'list_nature']
    path_file_in = file_project +"all_city_indicators.csv"

    with open(path_file_in, 'w',encoding="utf-8", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, field_order_move_in)
        writer.writeheader()
        for city_all_name_code,around_city_name  in zip(list_cityName,around_city):
            file_path = "F:/封城数据处理/paper_supplement_experiment/data/{0}/{1}/deal_03/".format(around_city_name,around_city_name+"一阶")
            list_avarge_node = averagenodeconnectivity(file_path,around_city_name,city_all_name_code)
            list_degree = get_city_degree(file_path,around_city_name,city_all_name_code)
            list_edge = edge_number(file_path,around_city_name,city_all_name_code)
            list_nature = naturecconnectivity(file_path,around_city_name,city_all_name_code)
            row = {"city_name": around_city_name, "level": "一阶", "list_avarge_node": list_avarge_node, "list_degree": list_degree, "list_edge": list_edge, "list_nature": list_nature}
            writer.writerow(row)



if __name__ == '__main__':
    # caculate_indicators()
    draw_all_city_indicators(20210101,20210508)









        # node_connectivity_alone(file_path,"石家庄",Five_order_SJZ)
        # average_degree_alone(file_path,"石家庄",Five_order_SJZ)

