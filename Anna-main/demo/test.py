
# coding:utf-8
"""
@file: around_city_flow.py
@author: wu hao
@time: 2022/11/20 14:45
@env: 封城数据处理
@desc:
@ref:
"""
import csv
import datetime

# coding=utf-8
import os

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter, MaxNLocator
from tqdm import tqdm
import numpy as np
from numpy import array
from sklearn.preprocessing import MinMaxScaler


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
#石家庄 封城时间 2021/1/7——2021/1/29日  比较时间2021/01/01 -2021/05/08(接近春节) 阈值选取为0.04 确定！

around_city=["北京","衡水","秦皇岛","唐山","廊坊","天津","承德","保定","沧州","邯郸","邢台","张家口"]
list_code_name =[['110000', '北京'], ['131100', '衡水'], ['130300', '秦皇岛'], ['130200', '唐山'], ['131000', '廊坊'], ['120000', '天津'], ['130800', '承德'], ['130600', '保定'], ['130900', '沧州'], ['130400', '邯郸'], ['130500', '邢台'], ['130700', '张家口']]

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

def find_code_and_name():
    list_final=[]
    for city in around_city:
        file = csv.reader(open('F:/封城数据处理/migrationof_BaiDu_spider/ChinaAreaCodes.csv', encoding="utf-8"))
        for row in file:
            if row[0] != 'code':
                if row[1] ==city:
                    listaaa=[]
                    code = row[0]
                    name = row[1]
                    listaaa.append(code)
                    listaaa.append(name)
                    list_final.append(listaaa)
                    break
    print(list_final)

def get_allCity_index():
    day_list = getdaylist(20210101,20210508)
    final_file_adress = "F:/封城数据处理/paper_supplement_experiment/data/所有城市迁徙指数/all_city_flow/all_city_index.csv"

    if not os.path.exists(final_file_adress):
        os.mkdir(final_file_adress)
    field_order_move_in = ["name", "value_in","value_out"]
    with open(final_file_adress, 'w',encoding="utf-8", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, field_order_move_in)
        writer.writeheader()
        for code_name in list_code_name:
            list_in_index = []
            list_out_index = []
            moveIn_file = "F:/封城数据处理/paper_supplement_experiment/data/所有城市迁徙指数/in/{0}_{1}_move_in.csv".format(code_name[0],code_name[1])
            moveOut_file = "F:/封城数据处理/paper_supplement_experiment/data/所有城市迁徙指数/out/{0}_{1}_move_out.csv".format(code_name[0],code_name[1])
            moveIn_data = pd.read_csv(moveIn_file,encoding="utf-8")
            moveOut_data = pd.read_csv(moveOut_file,encoding="utf-8")
            for data in day_list:
                for in_data in moveIn_data.iterrows():
                    if data == str(int(in_data[1]['date'])):
                        list_in_index.append(in_data[1]['index'])
                        break
                for out_data in moveOut_data.iterrows():
                    if data == str(int(out_data[1]['date'])):
                        list_out_index.append(out_data[1]['index'])
                        break
            row = {"name": code_name[1], "value_in": list_in_index,"value_out": list_out_index}
            writer.writerow(row)

def function_encapsulation(first_data,second_data,listXData):

    def format_fn(tick_val, tick_pos):
        if int(tick_val) in range(len(listXData)):
            return str(listXData[int(tick_val)])[4:8]
        else:
            return ''

    fig = plt.figure(figsize=(8, 6), dpi=450)
    ax = fig.add_subplot(111)
    ax.xaxis.set_major_formatter(FuncFormatter(format_fn))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    # plt.ylim((-5, 40))
    # 横坐标每个值旋转90度
    # plt.xticks(rotation=90)

    # 坐标轴ticks的字体大小
    ax.set_xlabel('日期', fontsize= 14)  # 为x轴添加标签
    ax.set_ylabel('数值', fontsize=14)  # 为y轴添加标签  数值
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    ax.legend()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # 根据需要设置最大最小值，这里设置最大值为1.最小值为0
    # 数据归一化
    tool = MinMaxScaler(feature_range=(0, 1))

    first_data = tool.fit_transform(array(first_data).reshape(-1,1)).tolist()
    second_data = tool.fit_transform(array(second_data).reshape(-1,1)).tolist()

    plt.title("全国疫情恢复情况")

    plt.plot(listXData, first_data,  linewidth=2, label='疫情搜索指数') #"4-",
    plt.plot(listXData, second_data, linewidth=2, label='健康问诊指数')#, "1--"




    plt.scatter(17, 1, s=50, color='cyan')
    plt.plot([17, 17], [1, 0], 'x--', lw=1.5)
    plt.text(17, 1, r'2022年12月21日', fontdict={'size': '14', 'color': 'black'})
    plt.legend()
    plt.show()
    #
    # plt.scatter(28, 1, s=50, color='cyan')
    # plt.plot([28, 28], [1, 0], 'x--', lw=1.5)
    # plt.text(27, 0.90, r'封城结束', fontdict={'size': '10', 'color': 'black'})

    # plt.scatter(92, 1, s=50, color='cyan')
    # plt.plot([92, 92], [1, 0], 'x--', lw=1.5)
    # plt.text(91, 0.90, r'清明节', fontdict={'size': '10', 'color': 'black'})
    #
    # plt.scatter(120, 1, s=50, color='cyan')
    # plt.plot([120, 120], [1, 0], 'x--', lw=1.5)
    # plt.text(119, 0.90, r'劳动节', fontdict={'size': '10', 'color': 'black'})



def draw_all_city_flow(beginData,endData):
    listXData = getdaylist(beginData, endData)
    fig = plt.figure(figsize=(16, 12), dpi=450)

    final_file_adress = "F:/封城数据处理/paper_supplement_experiment/data/所有城市迁徙指数/all_city_flow/all_city_index.csv"
    move_data = pd.read_csv(final_file_adress, encoding="utf-8")
    i=1
    for move_data in move_data.iterrows():
        city_name  = move_data[1]['name']
        value_in  = list(move_data[1]['value_in'][1:-1].split(","))
        value_out  = list(move_data[1]['value_out'][1:-1].split(","))
        ax = fig.add_subplot(4,3,i)

        # print(type(value_in))
        # print((value_in))
        # print(type(value_out))
        function_encapsulation(list(map(float, value_in)), list(map(float, value_out)), listXData,ax, city_name)
        i+=1

    plt.show()










if __name__ == '__main__':

    # fileName = "F:/疫情搜索指数数据/日常维护/辽宁省-大连市疫情大数据.csv"
    fileName = "F:/疫情搜索指数数据/日常维护/全国疫情大数据.csv"
    move_data = pd.read_csv(fileName, encoding="utf-8")
    search_index=[]
    health_index=[]
    for move_data in move_data.iterrows():
        search_index.append(move_data[1]['百度疫情搜索指数'])
        health_index.append(move_data[1]['百度健康问诊指数'])
    listXData = getdaylist(20221204,20230201)
    print(search_index)
    print(health_index)
    print(listXData)
    function_encapsulation(search_index,health_index,listXData)


























