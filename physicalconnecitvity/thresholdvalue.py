#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/11/23 14:46
# @Author  : wuhao
# @Email   : guess?????
# @File    : thresholdvalue.py
import time

import pandas as pd
import csv
import datetime

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
dayList = getdaylist(20200101,20211028)
# dayList = ["20210731","20210831","20210930"]
nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# 循环取每一天的值
for i in range(len(dayList)):
    print("开始处理数据==",dayList[i],"===当前时间为===",nowTime)
    # 迁入数据
    try:
        moveIn = pd.read_csv("F:\\01大连民族\\百度迁徙爬取和数据\\百度迁徙数据-final\\in\\"+dayList[i]+".csv")
    except Exception as problem:
        print("error打开迁入（in）有问题：", problem)
    else:
        df2 = moveIn[moveIn['num'] >= 0.04 ]
        df2.to_csv("F:\\01大连民族\\百度迁徙爬取和数据\\百度迁徙数据-final\\去掉0.04阈值后得数据\\in\\"+dayList[i]+".csv",index=None, encoding="utf_8_sig")
        nowTimeennd = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("结束时间",nowTimeennd)
#     data.columns = ["c", "d"]#直接在原数据上修改
