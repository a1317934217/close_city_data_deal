# coding:utf-8
"""
@file: caculate_allcity_down_propotion.py
@author: wu hao
@time: 2023/5/16 9:58
@env: 封城数据处理
@desc:
@ref:
"""
import csv
import datetime
from math import e
from math import log

# coding=utf-8
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter, MaxNLocator
# 根据路径画图
from sklearn.preprocessing import MinMaxScaler
from tqdm import tqdm
# 日期时间递增 格式yyyymmdd



def getdaylist(beginDate,endDate):
    beginDate = datetime.datetime.strptime(str(beginDate), "%Y%m%d")
    endDate = datetime.datetime.strptime(str(endDate), "%Y%m%d")
    dayList = []
    while beginDate <= endDate:
        dayList.append(datetime.datetime.strftime(beginDate, "%Y%m%d"))
        beginDate += datetime.timedelta(days=+1)
    return dayList

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
def averagenodeconnectivity(file_path,city_name,nodes,listXData):
    """
    返回绘制图表的
    X轴：日期
    Y轴：平均点连通性
    """

    listAverageNodeConnectivity = []
    for i in range(len(listXData)):
        # 循环画图
        try:
            filePathInMethon = file_path + listXData[i] +"_"+city_name+".csv"
            G = drawpicture(filePathInMethon,nodes)

        except Exception as problem:
            print("((平均点连通性) error打开迁徙文件出问题：", problem)
        else:
                listAverageNodeConnectivity.append((nx.average_node_connectivity(G)))
    # print("平均点连通性长度： ", len(listAverageNodeConnectivity))
    return listAverageNodeConnectivity
    # print("平均点连通性： ", listAverageNodeConnectivity)


# 计算城市度
def get_city_degree(file_path,city_name,nodes,listXData):
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
    return list_city_degree
    # print("城市度： ", list_city_degree)


# 计算边数量
def edge_number(file_path,city_name,nodes,listXData):
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
    return list_edge_number
    # print("边数量： ", list_edge_number)


# 计算自然连通性
def naturecconnectivity(file_path,city_name,nodes_list,listXData):
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
    return listAlgebraicConnectivity
    # print("自然连通度： ", listAlgebraicConnectivity)

def caculate_down_propotion(first_number,second_number):
    """
    计算时间顺序的下降比例
    :param first_number:  必须是列表参数的形式
    :param second_number: 必须是列表参数的形式
    :return:
    """
    # 衡量下降
    #最终储存的比例列表

    # 第一个
    num_old = 0
    for s in first_number:
        num_old = num_old + s
    # print(num_old)

    # 第二个
    num_new = 0
    for t in second_number:
        num_new = num_new + t
    # print(num_new)


    # result = (num_old - num_new) / num_new
    result = (num_old - num_new) / num_old

    return round(result, 4)

def getPreMonth(input_date,advance_days) :
    """

    :param input_date：开始时间
    :param advance_days:  提前的天数
    :return:
    """
    #注意输入要为 str形式
    #做转译
    s_date = input_date[:4]+"-"+input_date[4:6]+"-"+input_date[6:8]
    # 设置日期
    s_date = pd.Timestamp(s_date)
    # 获得前一月的这一天
    # 获得前一天
    #days = 1 mouths=1  在这里控制
    s_date1 = s_date + pd.DateOffset(n=-1, days=int(advance_days))
    #
    data_needdeal = str(s_date1)
    # print("前一月日期：", data_needdeal)
    #格式变换输出
    return int(data_needdeal[:10].replace("-",""))

list_cityone_hlbe =["齐齐哈尔","兴安盟","哈尔滨","黑河","呼和浩特","大兴安岭地区","大庆","北京","绥化","通辽","天津","赤峰","呼伦贝尔"]
list_cityone_sy =["长春","白城","四平","大庆","通辽","哈尔滨","吉林","沈阳","绥化","铁岭","齐齐哈尔","大连","松原"]
list_cityone_hh =["齐齐哈尔","绥化","哈尔滨","黑河","呼伦贝尔","伊春","大庆","大兴安岭","沈阳","佳木斯","大连","天津","营口"]
list_cityone_sh =["齐齐哈尔","大庆","哈尔滨","黑河","伊春","佳木斯","长春","北京","沈阳","大连","天津","松原","绥化"]
list_cityone_yz =["泰州","南京","淮安","镇江","滁州","苏州","盐城","无锡","常州","南通","宿迁","上海","扬州"]
list_cityone_zh =["长沙","湘潭","衡阳","萍乡","郴州","邵阳","娄底","益阳","岳阳","常德","深圳","株洲","广州"]
list_cityone_zy =["酒泉","兰州","嘉峪关","武威","海北藏族自治州","金昌","西宁","定西","西安","哈密","阿拉善","张掖","中卫"]
list_cityone_heb =["齐齐哈尔","绥化","哈尔滨","长春","佳木斯","大庆","北京","牡丹江","上海","天津","青岛","沈阳","鸡西"]
list_cityone_qqhe =["哈尔滨","呼伦贝尔","齐齐哈尔","兴安盟","大庆","黑河","天津","北京","绥化","白城","廊坊","沈阳","大连"]
list_cityone_sx =["杭州","宁波","金华","上海","嘉兴","温州","台州","苏州","湖州","衢州","无锡","南京","绍兴"]
list_cityone_xc =["郑州","平顶山","漯河","周口","开封","洛阳","南阳","商丘","新乡","驻马店","上海","许昌","苏州"]
list_cityone_zk =["郑州","商丘","阜阳","驻马店","漯河","金华","上海","许昌","北京","开封","苏州","杭州","周口"]
list_cityone_xy =["西安","宝鸡","渭南","铜川","延安","庆阳","榆林","平凉","商洛","汉中","上海","咸阳","安康"]
list_cityone_ts =["兰州","陇南","定西","西安","平凉","宝鸡","上海","苏州","北京","乌鲁木齐","杭州","天水","白银"]
list_name_around =[list_cityone_hlbe,list_cityone_sy,list_cityone_hh,list_cityone_sh,list_cityone_yz,
                   list_cityone_zh,list_cityone_zy,list_cityone_heb,list_cityone_qqhe,list_cityone_sx,list_cityone_xc,
                   list_cityone_zk,list_cityone_xy,list_cityone_ts]


def down_propotion_slice(list_lock_name,list_Unlock_name,city_name,lock_down_time):

    for lock_name,Unlock_name in zip(list_lock_name,list_Unlock_name):
        num_old = 0
        for s in lock_name:
            num_old = num_old + s
        # 第二个
        num_new = 0
        for t in Unlock_name:
            num_new = num_new + t
        # result = (num_old - num_new) / num_new
        result = (num_old - num_new) / num_new

        print_text = city_name + "======="+str(result)+ "封城时间天数===" +lock_down_time
        print(print_text)



def caculate_All_down_propotion():
    """
    封城城市的csv文件处理 得到封闭城市的指标的所有比例
    :return:
    """
    file_project = "F:/封城数据处理/封城数据/"
    file_lock_info = "F:/封城数据处理/封城数据/data_lockdown/lockdown_info.csv"
    with open(file_lock_info, 'r', encoding="utf-8") as file:
        reader = csv.reader(file, skipinitialspace=True)
        header = next(reader)
        for  row_one,list_aroundName in zip(reader,list_name_around):
            #城市名称
            city_name = row_one[0]
            # 开始封城时间
            start_date = int(row_one[1])#int
            end_date = int(row_one[2])#int
            #封城时间
            lockdown_day = row_one[3]
            # 城市阈值
            Threshold = float(row_one[4])
            # 一阶城市周围的城市
            # listaroundcity

            # 计算前面的时间
            data_oneMonth = getPreMonth(str(start_date),lockdown_day)

            file_path = "F:/封城数据处理/封城数据/{0}/{1}一阶/deal_03/".format(city_name,city_name)

            #封城时间段指标
            list_index_name_Lock = [averagenodeconnectivity(file_path,city_name , list_aroundName,getdaylist(start_date,end_date)),
                                    get_city_degree(file_path,city_name , list_aroundName,getdaylist(start_date,end_date)),
                                    edge_number(file_path,city_name , list_aroundName,getdaylist(start_date,end_date)),
                                    naturecconnectivity(file_path,city_name , list_aroundName,getdaylist(start_date,end_date))]
            # 封城前一段 时间段指标
            list_index_name_UnLock= [
                averagenodeconnectivity(file_path, city_name, list_aroundName, getdaylist(data_oneMonth, start_date)),
                get_city_degree(file_path, city_name, list_aroundName, getdaylist(data_oneMonth, start_date)),
                edge_number(file_path, city_name, list_aroundName, getdaylist(data_oneMonth, start_date)),
                naturecconnectivity(file_path, city_name, list_aroundName, getdaylist(data_oneMonth, start_date))]

            down_propotion_slice(list_index_name_Lock,list_index_name_UnLock,city_name,lockdown_day)








if __name__ == '__main__':
    caculate_All_down_propotion()


































