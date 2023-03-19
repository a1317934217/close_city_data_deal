# coding:utf-8
"""
@file: simple_deal.py
@author: wu hao
@time: 2023/2/28 15:17
@env: 封城数据处理
@desc:
@ref:
"""
import os
import time

import networkx as nx
import pandas as pd
import csv
import datetime
from tqdm import tqdm

# 主要城市GDP情况
file_path_source = "F:\封城数据处理\paper_supplement_experiment\data\主要城市月度价格.csv"

#源文件的处理情况
reference_file = "F:\\百度迁徙数据\\比例和指数计算完成后的数据\\in\\20211212.csv"



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




# 根据路径画图
def drawpicture(filePath,threshold,city):
    """
    输入文件路径最后绘制成图G
    """
    global dataMiga, G_return
    G = nx.Graph()
    try:
        dataMiga = pd.read_csv(filePath)
    except Exception as problem:
        print("error根据路径画图出现问题：", problem)
    # 得到每一行的数据
    for row in dataMiga.itertuples():
        city_name = getattr(row, "city_name")
        city_id_name = getattr(row, "city_id_name")
        num = getattr(row, "num")
        if float(num) >= float(threshold):
            G.add_edges_from([(city_name, city_id_name)])
    try:
        G_return = nx.ego_graph(G,city)
    except Exception as problem:
        print(problem)
    return G_return


# 最终确定自我中心城市
def get_around_city(city_list,time_list,threshold,file_migration,file_path_around_city_first,list_cityname_main_city,threshold_two):
    """
    找到自我中心网络的城市
    输入城市列表寻找他的高一阶城市
    :return:
    """
    #按照时间来生成  封闭城市  所对应的一阶自我中心网络的城市
    for time in time_list:
        with open(file_path_around_city_first+time+"_AroundCityName.csv", 'w', encoding="utf-8", newline='') as csvfile:
            # 表头
            file_order = ["city_name","点数量","边数量", 'city_around_list_name']
            writer = csv.DictWriter(csvfile, file_order)
            writer.writeheader()
            for city in city_list:

                G = drawpicture(file_migration+time+"_HaveRepeat.csv", threshold,city)
                print("城市名称：",city)
                print("时间：",time)
                print("城市个数：", len(G.nodes()))
                print("城市边集合：", len(G.edges()))
                row = {"city_name": city,"点数量":len(G.nodes()),"边数量":len(G.edges()), "city_around_list_name": G.edges()}
                writer.writerow(row)
            for city_two in list_cityname_main_city:
                G = drawpicture(file_migration+time+"_HaveRepeat.csv", threshold_two,city_two)
                print("城市名称：",city_two)
                print("时间：",time)
                print("城市个数：", len(G.nodes()))
                print("城市边集合：", len(G.edges()))
                row = {"city_name": city_two, "点数量":len(G.nodes()),"边数量":len(G.edges()),"city_around_list_name": G.edges()}
                writer.writerow(row)
            csvfile.close()






def deal_100_problem():
    """
    解决迁徙比例出现 忘记乘以100的问题
    :return:
    """
    # 寻找源头的文件
    file_migration_test = "F:/百度迁徙数据/比例和指数计算完成后的数据/out/"

    list_time_test = getdaylist(20220509, 20220830)
    for i in list_time_test:
        data = pd.read_csv(file_migration_test + i + ".csv")
        with open(file_migration_test + i + ".csv", 'w', encoding="utf-8", newline='') as csvfile:
            # 表头
            file_order = ["city_name", 'city_id_name', "num"]
            writer = csv.DictWriter(csvfile, file_order)
            writer.writeheader()
            for j in data.iterrows():
                num_first = float(j[1]["num"])
                num_finall = num_first * 100
                city_name = j[1]["city_name"]
                city_id_name = j[1]["city_id_name"]
                row = {"city_name": city_name, "city_id_name": city_id_name, "num": num_finall}
                writer.writerow(row)


#做取样标本，对in和out完全合并
def merge_in_out_2021(deal_time,file_migration):
    """
    属于第一步
    合并给定时间的整合数据
    :return:
    """

    # 创建处理完的数据csv
    # 表头
    field_order_move_in = ["city_name", 'city_id_name', 'num']
    # 开始写入整理完的数据csv
    move_in_data = pd.read_csv(file_migration + "in/"+deal_time+".csv")
    move_out_data = pd.read_csv(file_migration + "out/"+deal_time+".csv")
    with open("F:/封城数据处理/paper_supplement_experiment/data/"+deal_time+"_HaveRepeat.csv", 'w',
              encoding="utf-8", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, field_order_move_in)
        writer.writeheader()
        for row_in in tqdm(move_in_data.iterrows(),desc="in和out合并",total=len(move_in_data)):
            city_name_one = row_in[1]["city_name"]
            city_name_two = row_in[1]["city_id_name"]
            value_one = row_in[1]["num"]
            compare_str_one = city_name_two+","+city_name_one
            for row_out in move_out_data.iterrows():
                city_name_three = row_out[1]["city_name"]
                city_name_four = row_out[1]["city_id_name"]
                value_two = row_out[1]["num"]
                compare_str_two = city_name_three + "," + city_name_four
                if compare_str_one == compare_str_two:
                    row = {"city_name": city_name_three, "city_id_name": city_name_four, "num": (float(value_one)+float(value_two))/2}
                    writer.writerow(row)
                    break







if __name__ == '__main__':
    #时间序列
    list_time = ['20230112', '20221212', '20221112', '20221012', '20220912', '20220812', '20220712', '20220612','20220512', '20220412', '20220312', '20220212', '20220112', '20211212', '20211112', '20211012','20210912', '20210812', '20210712', '20210612', '20210512', '20210412', '20210312', '20210212','20210112', '20201212', '20201112', '20201012']

    #'20220912',
    # list_time=[ '20210212']

    #需要找一节自我中心的城市的城市
    list_cityName = [ '天津','石家庄', '太原', '呼和浩特', '沈阳', '大连', '长春', '哈尔滨',  '杭州', '宁波', '合肥', '福州', '厦门','南昌', '济南', '青岛', '郑州', '武汉', '长沙',  '南宁', '海口',  '贵阳', '昆明', '拉萨', '西安','兰州', '西宁', '银川', '乌鲁木齐']
    list_cityname_main_city = ['北京','上海',  '南京','广州', '深圳','重庆', '成都']


    #寻找构建网络的文件
    file_migration= "F:/封城数据处理/paper_supplement_experiment/data/merge_complete/"

    #生成的一阶自我中心网络城市集合
    file_path_around_city_first ="F:/封城数据处理/paper_supplement_experiment/data/city_around_by_time/"


    #生成最终需要的城市csv
    get_around_city(list_cityName,list_time, 0.04,file_migration,file_path_around_city_first,
                    list_cityname_main_city,0.08)


    #合并in和out的数据  一开始处理的数据问题
    # for time in list_time:
    #     merge_in_out_2021(time,file_migration)


































