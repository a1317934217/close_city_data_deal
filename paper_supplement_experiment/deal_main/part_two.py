# coding:utf-8
"""
@file: part_two.py
@author: wu hao
@time: 2022/11/7 16:26
@env: 封城数据处理
@desc:
@ref:
"""
import datetime

# coding=utf-8
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter, MaxNLocator
import numpy as np
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
yuzhi_list = [0.0, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.07, 0.075,
                  0.08, 0.085, 0.09, 0.095, 0.1, 0.105, 0.11, 0.115, 0.12, 0.125, 0.13, 0.135, 0.14, 0.145, 0.15, 0.155,
                  0.16, 0.165, 0.17, 0.17500000000000002, 0.18, 0.185, 0.19, 0.195, 0.2, 0.20500000000000002, 0.21,
                  0.215, 0.22, 0.225, 0.23, 0.23500000000000001, 0.24, 0.245, 0.25]
city_number = [377, 370, 368, 363, 362, 336, 334, 326, 323, 318, 304, 291, 283, 273, 267, 266, 237, 165, 139, 107, 93, 84, 84, 84, 82, 82, 78, 77, 63, 62, 61, 33, 33, 33, 27, 26, 23, 22, 21, 21, 19, 19, 19, 19, 19, 19, 19, 18, 18, 14, 14]

weakly_number = [22, 23, 24, 28, 29, 34, 39, 42, 45, 51, 54, 58, 66, 75, 82, 87, 92, 104, 112, 120, 126, 129, 134, 143, 148, 155, 165, 172, 180, 184, 192, 194, 196, 200, 205, 209, 214, 215, 220, 226, 232, 236, 239, 242, 244, 247, 250, 254, 257, 261, 263]

def draw_every_indeicators(lable_x,first_data,second_data):
    """
    画阈值的方法
    :param lable_x:
    :param first_data:
    :param second_data:
    :return:
    """

    # 画图 设置X轴显示效果
    # 为了设置x轴时间的显示
    def format_fn(tick_val, tick_pos):
        if int(tick_val) in range(len(lable_x)):
            return lable_x[int(tick_val)]
        else:
            return ''

    plt.rcParams['font.sans-serif'] = ['SimHei']
    x = np.arange(0, 51, 1)

    # fig = plt.figure(figsize=( 12, 4))
    fig = plt.figure(figsize=( 6, 4))

    # plt.rcParams['figure.figsize'] = (8, 16)
    plt.rcParams['savefig.dpi'] = 1200  # 图片像素
    plt.rcParams['figure.dpi'] = 1200
    #


    ax1 = fig.add_subplot(111)
    # ax1.xaxis.set_major_formatter(FuncFormatter(format_fn))
    # ax1.xaxis.set_major_locator(MaxNLocator(integer=True))

    aaaaaa=[0.00,0.05,0.10,0.15,0.20,0.25]
    plt.xticks(aaaaaa)

    # 坐标轴ticks的字体大小
    ax1.set_xlabel('阈值', fontsize=12)  # 为x轴添加标签
    ax1.set_ylabel('城市节点个数', fontsize=12)  # 为y轴添加标签  数值


    plt.plot(lable_x,first_data, "4-", linewidth=2, label='最大连接组件内城市数量')
    plt.plot(lable_x,second_data, "1--", linewidth=2, label='弱连接组件数量')

    ax1.legend(prop = {'size':12})

    plt.show()






if __name__ == '__main__':
    draw_every_indeicators(yuzhi_list,city_number,weakly_number)




