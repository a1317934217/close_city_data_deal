"""
@file: test.py
@author: wu hao
@time: 2022/9/26 10:19
@env: 封城数据处理
@desc:
@ref:
"""
import pandas as pd
import networkx as nx
reference_file = r"F:\封城数据处理\封城数据\main_deal\data\20210101_merge.csv"

cc = pd.read_csv(reference_file)
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
        G.add_edges_from([(city_name, city_id_name)])
    return G