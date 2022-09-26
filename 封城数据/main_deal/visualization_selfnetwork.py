# coding:utf-8
"""
@file: visualization_selfnetwork.py
@author: wu hao
@time: 2022/9/26 21:38
@env: 封城数据处理
@desc:
@ref:
"""
import matplotlib
import pandas as pd
import csv
import datetime
import networkx as nx
import numpy as np
import pandas as pd
# coding=utf-8
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import FuncFormatter, MaxNLocator
import matplotlib.pyplot as plt





# 根据路径画图
def drawpicture(filePath):
    """
    输入文件路径最后绘制成图G
    """
    global dataMiga
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
        G.add_edges_from([(city_name, city_id_name)])
    return G


plt.rcParams["font.sans-serif"]=["SimHei"] #设置字体
plt.rcParams["axes.unicode_minus"]=False #该语句解决图像中的“-”负号的乱码问题
plt.rcParams['figure.figsize']= (24, 24)
filePath = "F:\封城数据处理\封城数据\石家庄\石家庄二阶\garbage_self_network" \
           "\deal_03\\20210101_石家庄.csv"

G = drawpicture(filePath)
pos = nx.circular_layout(G)

pos["石家庄"]=[0,0]
nx.draw(G,pos,with_labels = True,node_size=40)
plt.show()