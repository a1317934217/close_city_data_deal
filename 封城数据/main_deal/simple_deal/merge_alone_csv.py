# coding:utf-8
"""
@file: merge_alone_csv.py
@author: wu hao
@time: 2023/6/16 15:43
@env: 封城数据处理
@desc:
@ref:
"""
import csv
import os

import pandas as pd
from tqdm import tqdm
import datetime
def getdaylist(beginDate,endDate):
    beginDate = datetime.datetime.strptime(str(beginDate), "%Y%m%d")
    endDate = datetime.datetime.strptime(str(endDate), "%Y%m%d")
    dayList = []
    while beginDate <= endDate:
        dayList.append(datetime.datetime.strftime(beginDate, "%Y%m%d"))
        beginDate += datetime.timedelta(days=+1)
    return dayList


def compare_two_str(a,b):
    if len(a) != len(b):
        return False
    return sorted(a) == sorted(b)




def merge_alone_file(beginTime,endTime,cityName,file_project):
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
        need_deal_file_one = pd.read_csv(file_project  + dayList[i] + "_"+cityName+".csv")
        need_deal_file_two = pd.read_csv(file_project  + dayList[i] + "_"+cityName+".csv")
        length = len(need_deal_file_one)
        with open(file_project + dayList[i] + "_"+cityName+".csv", 'w',
                  encoding="utf-8", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, field_order_move_in)
            writer.writeheader()
            # for i in range(length):

            for i in range(length):
                df1 = need_deal_file_one.loc[i]
                list_a = []
                city_name_one = df1["city_name"]
                city_name_two = df1["city_id_name"]
                value_one = df1["num"]
                list_a.append(city_name_one)
                list_a.append(city_name_two)
                # print("one:",i)
                for j in range(length - i - 1):
                    # print("two:",j+i+1)
                    df2 = need_deal_file_one.loc[j + i + 1]
                    list_b = []
                    city_name_three = df2["city_name"]
                    city_name_four = df2["city_id_name"]
                    value_two = df2["num"]
                    list_b.append(city_name_three)
                    list_b.append(city_name_four)
                    if compare_two_str(list_a, list_b):
                        valueColThree = (float(value_one) + float(value_two)) / 2
                        row = {"city_name": city_name_three, "city_id_name": city_name_four, "num": valueColThree}
                        writer.writerow(row)
                        break

file_project="F:/封城数据处理/封城数据/石家庄/石家庄一阶/deal_03/"
merge_alone_file(20201201,20210508, "石家庄", file_project)
# aaa= ["北京","石家庄"]
# bbb= ["北京","石家庄"]
# print(compare_two_str(aaa, bbb))

# need_deal_file_one = pd.read_csv(file_project + "20210101_石家庄.csv")
#
# length = len(need_deal_file_one)


#
#
# for i in range(length):
#     df1 = need_deal_file_one.loc[i]
#     list_a = []
#     city_name_one = df1["city_name"]
#     city_name_two = df1["city_id_name"]
#     value_one = df1["num"]
#     list_a.append(city_name_one)
#     list_a.append(city_name_two)
#     # print("one:",i)
#     for j in range(length-i-1):
#         # print("two:",j+i+1)
#         df2 = need_deal_file_one.loc[j+i+1]
#         list_b = []
#         city_name_three = df2["city_name"]
#         city_name_four = df2["city_id_name"]
#         value_two = df2["num"]
#         list_b.append(city_name_three)
#         list_b.append(city_name_four)
#         if compare_two_str(list_a, list_b):
#             valueColThree = (float(value_one) + float(value_two)) / 2
#             print(city_name_three,city_name_four,str(valueColThree))


































