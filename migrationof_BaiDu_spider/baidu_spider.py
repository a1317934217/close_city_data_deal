#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/1/13 14:09
# @Author  : wuhao
# @Email   : guess?????
# @File    : baidu_spider.py
# coding:utf-8
import csv
import datetime
import json
import os

import re

import requests

#json解析
from tqdm import tqdm


def loads_jsonp(_jsonp):
    try:
        return json.loads(re.match(".*?({.*}).*", _jsonp, re.S).group(1))
    except:
        raise ValueError('Invalid Input')

#  获取时间列表
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


# 城市迁徙比例数据保存路径 in
migration_proportion_in = 'F:/百度迁徙数据_日常维护/迁徙比例/in/'
# 城市迁徙比例数据保存路径 out
migration_proportion_out = 'F:/百度迁徙数据_日常维护/迁徙比例/out/'

# 城市迁徙指数数据保存路径 in
migration_index_in = 'F:/百度迁徙数据_日常维护/迁徙指数/in/'
# 城市迁徙指数数据保存路径 out
migration_index_out = 'F:/百度迁徙数据_日常维护/迁徙指数/out/'


# 爬取迁徙指数 文件
def get_city_migration_index(file_save_location,task_type):
    """
    爬取迁徙指数 文件
    :param file_save_location:  文件保存位置
    :param task_type:  迁徙类型 in or out
    :return:
    """
    global text
    file = csv.reader(open('ChinaAreaCodes.csv',encoding="utf-8"))
    for row in tqdm(file,desc="迁徙指数进度条和类型："+task_type,total=375):
        if row[0] != 'code':
            code = row[0]
            name = row[1]
            try:
                #示例url爬取
                # url = "https://huiyan.baidu.com/migration/historycurve.jsonp?dt=city&id=110000&type=move_in"
                url = 'https://huiyan.baidu.com/migration/historycurve.jsonp?dt=city&id={}&type={}'.format(code, task_type)
                #整合数据
                # url = 'https://huiyan.baidu.com/migration/historycurve.jsonp?dt=city&id={}&type={}&startDate=20200110&endDate=20200315'.format(code, task_type)
                try:
                    # https://huiyan.baidu.com/migration/historycurve.jsonp?dt=city&id=110000&type=move_in
                    text = loads_jsonp(requests.get(url).text)
                except:
                    print(name+"：no data")
                # print(text)
                data = text['data']['list']
                #生成excel的头部
                header = ['date', 'index']
                with open(file_save_location + '{}_{}_{}.csv'.format(code, name, task_type), "w+", newline="",encoding='utf_8_sig') as csv_file:
                    writer=csv.writer(csv_file)
                    writer.writerow(header)
                    for key, values in data.items():
                        row = [key, values]
                        writer.writerow(row)
                # print(code + 'is OK')
            except Exception as why:
                print(why)
                print(code + ' No Data')
# 爬取城市迁徙比例 文件
def get_city_migration_proportion(file_save_location,task_type,beginTime,endTime):
    """
    爬取城市迁徙比例 文件
    :param file_save_location: 文件保存路径
    :param task_type:
    :param beginTime:
    :param endTime:
    :return:
    """

    # 获得时间列表
    timeList = getdaylist(beginTime,endTime)
    file = csv.reader(open('ChinaAreaCodes.csv',encoding="utf-8"))
    for row in tqdm(file,desc="迁徙比例进度条和类型"+task_type,total=375):
        if row[0] != 'code':
            code = row[0]
            name = row[1]
            try:
                for t in timeList:


                    #https://huiyan.baidu.com/migration/cityrank.jsonp?dt=city&id=130100&type=move_in&date=20210308&startDate=20210109&endDate=20210308



                    # 迁徙比例
                    # url = 'https://huiyan.baidu.com/migration/cityrank.jsonp?dt=city&id=110000&type=move_in&date=20211029'
                    url = 'https://huiyan.baidu.com/migration/cityrank.jsonp?dt=city&id={}&type={}&date={}'.format(code,task_type,t)
                    # url = 'https://huiyan.baidu.com/migration/cityrank.jsonp?dt=city&id={}&type={}&date={}&startDate=20200922&endDate=20210118'.format(code,task_type,t)
                    try:
                        # requests.adapters.DEFAULT_RETRIES = 5
                        data = loads_jsonp(requests.get(url).text)['data']["list"]
                        header = ['city_name', 'value']
                        with open(file_save_location + '{}_{}_{}_{}.csv'.format(code,name, task_type, t,encoding="utf_8_sig"), "w+",
                                  newline="") as csv_file:
                            writer = csv.writer(csv_file)
                            writer.writerow(header)
                            for text_val in data:
                                row = [text_val['city_name'],text_val['value']/100]
                                writer.writerow(row)
                    except Exception as reason:
                        print(code,name,t,reason,"no data")
            except Exception as why:
                print(why)
                print(code + ' No Data')




def makeUp_problem_data(file_save_location,task_type,code,name,t):
    """
    一定要注意url格式！！！！！！！！！ 可能有爬取一段时间的
    :param file_save_location:
    :param task_type:
    :param code:
    :param name:
    :param t:
    :return:
    """
    # url = 'https://huiyan.baidu.com/migration/cityrank.jsonp?dt=city&id={}&type={}&date={}&startDate=20200922&endDate=20210118'.format(code, task_type, t)
    url = 'https://huiyan.baidu.com/migration/cityrank.jsonp?dt=city&id={}&type={}&date={}'.format(code, task_type, t)
    try:
        # requests.adapters.DEFAULT_RETRIES = 5
        data = loads_jsonp(requests.get(url).text)['data']["list"]
        header = ['city_name', 'value']
        with open(file_save_location + '{}_{}_{}_{}.csv'.format(code, name, task_type, t, encoding="utf_8_sig"), "w+",
                  newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(header)
            for text_val in data:
                row = [text_val['city_name'], text_val['value'] / 100]
                writer.writerow(row)
    except Exception as reason:
        print(code, name, t, reason, "no data")




# #

def rename_csv(begindata,enddata):
    """
    批量更改文件名字
    :param begindata:
    :param enddata:
    :return:
    """
    timeList = getdaylist(begindata,enddata)
    for time_i in timeList:
        fileName_file_old = "F:\\01大连民族\百度迁徙爬取和数据\百度迁徙数据更新_经常运行\迁徙比例\out\\220200_吉林市_move_out_{0}.csv".format(time_i)
        fileName_file_new = "F:\\01大连民族\百度迁徙爬取和数据\百度迁徙数据更新_经常运行\迁徙比例\out\\220200_吉林_move_out_{0}.csv".format(time_i)
        try:
            os.rename(fileName_file_old,fileName_file_new)
        except Exception as problem:
            print("error打开迁徙指数有问题：", problem)



if __name__ == '__main__':


    #两个迁徙指数 爬取
    # get_city_migration_index(migration_index_in,"move_in")
    # get_city_migration_index(migration_index_out,"move_out")


    # get_city_migration_index("F:/百度迁徙数据_日常维护/迁徙指数_需补充/in/", "move_in")
    # get_city_migration_index('F:/百度迁徙数据_日常维护/迁徙指数_需补充/out/', "move_out")


    #两个迁徙比例 爬取
    get_city_migration_proportion(migration_proportion_in,"move_in",20230225,20230508)
    get_city_migration_proportion(migration_proportion_out,"move_out",20230225,20230508)


    #补充爬取

    # list_problem_in = [(469001, "五指山", 20221123),(530400, "玉溪", 20221108)]
    # list_problem_out = [(210900, "阜新", 20221013), (370300, "淄博", 20221205)]
    #
    # for i in list_problem_in:
    #     makeUp_problem_data(migration_proportion_in,"move_in",i[0],i[1],i[2])
    #
    # for i in list_problem_out:
    #     makeUp_problem_data(migration_proportion_out,"move_out",i[0],i[1],i[2])






