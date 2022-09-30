# coding:utf-8
"""
@file: igraph_selfnetwork.py
@author: wu hao
@time: 2022/9/29 15:45
@env: 封城数据处理
@desc:
@ref:
"""

import igraph as ig
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
# Set configuration variables
ig.config["plotting.backend"] = "matplotlib"
ig.config["plotting.layout"] = "fruchterman_reingold"
ig.config["plotting.palette"] = "rainbow"

# Save configuration to ~/.igraphrc
ig.config.save()

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



file_path = "F:/封城数据处理/封城数据/西安/西安二阶/deal_03/20211209_西安.csv"
nodes_xa =  ['临汾', '兰州', '廊坊', '呼和浩特', '汉中', '延安', '铜川', '西安', '宜宾', '周口', '上海', '榆林', '遂宁', '成都', '石家庄', '广元', '凉山彝族自治州', '达州', '白银', '邯郸', '庆阳', '攀枝花', '邢台', '济南', '衡水', '张家口', '新乡', '洛阳', '贵阳', '沈阳', '焦作', '广安', '阿坝藏族羌族自治州', '沧州', '莱芜', '雅安', '开封', '甘南藏族自治州', '保定', '自贡', '眉山', '青岛', '商丘', '濮阳', '甘孜藏族自治州', '天津', '乐山', '武汉', '南阳', '南京', '安阳', '资阳', '三门峡', '南充', '巴中', '信阳', '临夏回族自治州', '吕梁', '咸阳', '昆明', '秦皇岛', '绵阳', '定西', '驻马店', '漯河', '商洛', '泸州', '运城', '宝鸡', '平顶山', '许昌', '重庆', '鹤壁', '唐山', '郑州', '北京', '天水', '太原', '渭南', '承德', '安康', '深圳', '德阳', '武威', '鄂尔多斯', '忻州', '银川', '西宁', '内江']
plt.rcParams['font.sans-serif'] = ['SimHei']

def igraph_method():
    G = drawpicture(file_path)
    g = ig.Graph()
    g.add_vertices(nodes_xa)
    g.add_edges(G.edges())
    # layout = g.layout_circle()

    g.vs["label"] = g.vs["name"]
    g.vs["label_size"] = 12
    g.vs["label_color"] = "blue"
    # betweenness = g.betweenness() ,vertex_color=colors
    # colors = [int(i * 200 / max(betweenness)) for i in betweenness]
    ig.plot(g,bbox=(500, 500), margin=20, vertex_size=0.2, edge_width=0.5)
    plt.show()



if __name__ == '__main__':
    igraph_method()







# g = ig.Graph.Barabasi(n=len(G.nodes()), m=1)
# # Calculate a color value between 0-200 for all nodes
# betweenness = g.betweenness()
# colors = [int(i * 200 / max(betweenness)) for i in betweenness]
# # Plot the graph
# ig.plot(g, vertex_color=colors, vertex_size=1, edge_width=0.3)
# plt.show()