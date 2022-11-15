# coding:utf-8
"""
@file: test.py
@author: wu hao
@time: 2022/10/28 14:49
@env: 封城数据处理
@desc:
@ref:
"""
import xlrd

# 打开文件
from pandas import DataFrame
import numpy as np
import matplotlib.pyplot as plt
import random
data = xlrd.open_workbook('F:/封城数据处理/SODA_Match/data/train_data.xls')



# 通过文件名获得工作表,获取工作表1
table = DataFrame(data.sheet_by_name('机械设备故障预测数据集'))
# print(table)
# print(table.describe())
print(table[2].value_counts())
x_lo = ["0","1"]
y_lo = [8301,8301]
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False


def drawpic(X,Y):
    # 准备数据
    x_data = X
    y_data = Y

    plt.bar(x_data, y_data)
    # 设置图片名称
    plt.title("目标值样本分布（处理后）")
    # 设置x轴标签名
    plt.xlabel("")
    # 设置y轴标签名
    plt.ylabel("数值")
    # 显示
    plt.show()
    # 正确显示中文和负号


if __name__ == '__main__':
    drawpic(x_lo,y_lo)
