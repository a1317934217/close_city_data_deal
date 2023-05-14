# coding:utf-8
"""
@file: caculate_indicators_poption.py
@author: wu hao
@time: 2023/5/14 16:30
@env: 封城数据处理
@desc:
@ref:
"""
import datetime
import calendar
import time

import pandas as pd
def getPreMonth(input_date) :

    #做转译
    s_date = input_date[:4]+"-"+input_date[4:6]+"-"+input_date[6:8]
    # 设置日期
    s_date = pd.Timestamp(s_date)
    # 获得前一月的这一天
    s_date1 = s_date + pd.DateOffset(n=-1, months=1)
    #
    data_needdeal = str(s_date1)
    # print("前一月日期：", data_needdeal)
    #格式变换输出
    return int(data_needdeal[:10].replace("-",""))


if __name__ == '__main__':
    print(type(getPreMonth(str(20200101))))
    print((getPreMonth(str(20200101))))
























