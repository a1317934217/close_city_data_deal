#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/11/23 16:04
# @Author  : wuhao
# @Email   : guess?????
# @File    : demo2107.py
import time

import pandas as pd
import csv
import datetime

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
    #得到时间
        ######在这里修改要处理的时间的数据
        ##=========
        ##-------
dayList = getdaylist(20210701,20210731)
# dayList = ["20200101"]
# 循环取每一天的值
for i in range(len(dayList)):
    nowTimebegin = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("开始处理数据==",dayList[i],"===当前时间为===",nowTimebegin)
    # 迁入数据
    try:
        moveIn = pd.read_csv("F:\\01大连民族\\百度迁徙爬取和数据\\百度迁徙数据-final\\去掉0.04阈值后得数据\\in\\"+dayList[i]+".csv")
    except Exception as problem:
        print("error打开迁入（in）有问题：", problem)
        continue
    # 迁出数据
    try:
        moveOut = pd.read_csv("F:\\01大连民族\\百度迁徙爬取和数据\\百度迁徙数据-final\\去掉0.04阈值后得数据\\out\\" + dayList[i] + ".csv")
    except Exception as problem:
        print("error打开迁出（out）有问题：", problem)
        continue

    # 创建处理完的数据csv
    # 表头
    field_order_move_in = ["city_name", 'city_id_name', 'num']
    # 开始写入整理完的数据csv
    with open("F:\\01大连民族\\百度迁徙爬取和数据\\百度迁徙数据-final\\物理联通指标所需数据\\" + dayList[i] + "physical.csv", 'w',
              encoding="utf-8", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, field_order_move_in)
        writer.writeheader()
        # move_in 每一行
        # 提高运算效率。简化数据，指标
        index_data =0
        for moveOut_city in range(moveIn["city_name"].count()):
            # 使用列表比较是否相同move_in
            listMoveIn = []
            indexColMoveIn = moveIn.loc[moveOut_city]
            listMoveIn.append(indexColMoveIn[0])
            listMoveIn.append(indexColMoveIn[1])
            # move_out 每一行
            for j in range(moveOut["city_name"].count()):
                # 使用列表比较是否相同move_out
                listMove_out = []
                indexColMoveOut = moveOut.loc[j]
                listMove_out.append(indexColMoveOut[0])
                listMove_out.append(indexColMoveOut[1])
                # 获取到索引
                indexMoveOutNumber = moveOut[(moveOut.city_name == indexColMoveOut[0]) & (moveOut.city_id_name == indexColMoveOut[1])].index.tolist()[0]
                # 判断两个列表是否相同 ，来进value值相加除二
                if compare_two_str(listMoveIn,listMove_out):
                    valueColThree = (indexColMoveIn[2] + indexColMoveOut[2])/2
                    row = {"city_name": indexColMoveIn[0], "city_id_name": indexColMoveIn[1], "num": valueColThree}
                    writer.writerow(row)
                    moveOut.drop(indexMoveOutNumber,axis=0,inplace=True)
                    # print("移除数据",indexColMoveOut)
                    moveOut = moveOut.reset_index(drop=True)
                    index_data += 1
                    break
    nowTimeEnd = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(dayList[i],"这天的数据处理完后的时间为",nowTimeEnd)
    csvfile.close()