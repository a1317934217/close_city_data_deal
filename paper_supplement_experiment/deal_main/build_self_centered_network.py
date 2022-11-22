# -*- coding: utf-8 -*-
"""
#!/usr/bin/env python

@file: generate_csv_file.py
@author: wu hao
@time: 2022/9/26 9:27
@env: 封城数据处理
@desc:
@ref:石家庄阈值0.04，西安阈值0.08
"""
import os
import time

import networkx as nx
import pandas as pd
import csv
import datetime
from tqdm import tqdm
#迁徙数据位置
fileNameFront = "F:/百度迁徙数据/比例和指数计算完成后的数据/"
#处理后存储的位置
file_project =  r"F:/封城数据处理/paper_supplement_experiment/data/"

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


around_city_alone=["张家口"]
alon_list =[zhangjiakou_one_network]






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


def select_around_city_data(beginTime,endTime,around_city,rank_level):
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
        path_file_in = file_project+rank_level[:-2]+"/"+rank_level+"/deal_01/in/"
        if not os.path.exists(path_file_in):
            os.makedirs(path_file_in)
        with open(path_file_in + dayList[i] + "_{}.csv".format(rank_level[:-2]), 'w',encoding="utf-8", newline='') as csvfile:

            writer = csv.DictWriter(csvfile, field_order_move_in)
            writer.writeheader()
            # move_in 每一行
            for row_in in moveIn.itertuples():
                city_name = getattr(row_in, "city_name")
                city_id_name = getattr(row_in, "city_id_name")
                num = getattr(row_in, "num")
                if num >=0.04:
                    if city_name in around_city and city_id_name in around_city:
                        row = {"city_name": city_name, "city_id_name": city_id_name, "num": num}
                        writer.writerow(row)
            csvfile.close()
            path_file_out = file_project +rank_level[:-2]+"/"+rank_level+ "/deal_01/out/"
            if not os.path.exists(path_file_out):
                os.mkdir(path_file_out)
            with open(path_file_out+ dayList[i] + "_{}.csv".format(rank_level[:-2]), 'w',encoding="utf-8", newline='') as csvfile:
                writer = csv.DictWriter(csvfile, field_order_move_in)
                writer.writeheader()
                # move_in 每一行
                for row_out in moveOut.itertuples():
                    city_name = getattr(row_out, "city_name")
                    city_id_name = getattr(row_out, "city_id_name")
                    num = getattr(row_out, "num")
                    if num >= 0.04:
                        if city_name in around_city and city_id_name in around_city:
                            row = {"city_name": city_name, "city_id_name": city_id_name, "num": num}
                            writer.writerow(row)
                csvfile.close()


def merge_inAndout_file(beginTime,endTime,rank_level):
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
        move_in_data = pd.read_csv(file_project+rank_level[:-2]+"/"+rank_level+"/deal_01/in/"+dayList[i]+"_{}.csv".format(rank_level[:-2]))
        move_out_data = pd.read_csv(file_project+rank_level[:-2]+"/"+rank_level+"/deal_01/out/"+dayList[i]+"_{}.csv".format(rank_level[:-2]))
        path_file_in = file_project +rank_level[:-2]+"/"+rank_level + "/deal_02/"
        if not os.path.exists(path_file_in):
            os.makedirs(path_file_in)
        with open(path_file_in+ dayList[i] + "_{}.csv".format(rank_level[:-2]), 'w',
                  encoding="utf-8", newline='') as csvfile:
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


def merge_alone_file(beginTime,endTime,rank_level):
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
        need_deal_file_one = pd.read_csv(file_project +rank_level[:-2]+"/"+rank_level+ "/deal_02/" + dayList[i] + "_{}.csv".format(rank_level[:-2]))
        need_deal_file_two = pd.read_csv(file_project +rank_level[:-2]+"/"+rank_level+ "/deal_02/" + dayList[i] + "_{}.csv".format(rank_level[:-2]))
        path_file_in = file_project +rank_level[:-2]+"/"+ rank_level + "/deal_03/"
        if not os.path.exists(path_file_in):
            os.makedirs(path_file_in)
        with open(path_file_in + dayList[i] + "_{}.csv".format(rank_level[:-2]), 'w',
                  encoding="utf-8", newline='') as csvfile:
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



if __name__ == '__main__':

    for city_all_name_code,around_city_name  in zip(list_cityName,around_city):

        select_around_city_data(20210101,20210508,city_all_name_code,"{}一阶".format(around_city_name))
        merge_inAndout_file(20210101,20210508, "{}一阶".format(around_city_name))
        merge_alone_file(20210101,20210508,"{}一阶".format(around_city_name))

