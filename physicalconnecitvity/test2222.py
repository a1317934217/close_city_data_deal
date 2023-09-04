#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/11/14 10:39
# @Author  : wuhao
# @Email   : guess?????
# @File    : test2222.py
from math import e
from math import log
from networkx.algorithms.connectivity import minimum_st_node_cut, minimum_node_cut
from networkx.algorithms.flow import shortest_augmenting_path
from networkx.algorithms.flow import shortest_augmenting_path
from networkx.algorithms.connectivity import minimum_st_node_cut

from networkx.algorithms.connectivity import local_edge_connectivity
from networkx.algorithms.connectivity import local_node_connectivity
import networkx as nx
import matplotlib.pyplot as plt
from networkx import laplacian_matrix
from numpy import array
import numpy as np
from networkx.algorithms import approximation as approx
from networkx.algorithms.connectivity import minimum_st_node_cut
import  pandas as pd
G = nx.Graph()
G1 = nx.Graph()
G.add_node("A",desc="A")
G.add_node("B",desc="B")
G.add_node("C",desc="C")
G.add_node("D",desc="D")
G.add_node("E",desc="E")
G.add_node("F",desc="F")
# G.add_node("G",desc="G")
G.add_edges_from([("A","B") ,("A" ,"C") ,("A" ,"D") ,("A" ,"E"),("B" ,"C"),("B","D")
                  ,("B" ,"E"),("D" ,"C"),("E" ,"C"),("D" ,"E"),("F" ,"A"),("F" ,"B")
                     ,("F" ,"C")])


# G1.add_node("A",desc="A")
# G1.add_node("B",desc="B")
# G1.add_node("C",desc="C")
# G1.add_node("D",desc="D")
# G1.add_node("E",desc="E")
# # G.add_node("F",desc="F")
# # G.add_node("G",desc="G") ,("B" ,"D")
# G1.add_edges_from([("A","B") ,("A" ,"D") ,("C" ,"B") ,("C" ,"D")])

pos = nx.circular_layout(G)
nx.draw(G,pos)
mode_labels = nx.get_node_attributes(G,'desc')
nx.draw_networkx_nodes(G,pos,label=mode_labels)
plt.show()
#
# pos = nx.circular_layout(G1)
# nx.draw(G1,pos)
# mode_labels = nx.get_node_attributes(G1,'desc')
# nx.draw_networkx_nodes(G1,pos,label=mode_labels)
# plt.show()

# dela_first_list = list(set(G)^set(G1))
# print(dela_first_list)
# print(len(dela_first_list))






# number_one = nx.number_connected_components(G)
# S = [G.subgraph(c).copy() for c in nx.connected_components(G)]
#
# short_length = nx.global_efficiency(G)
# print("最短路径：", short_length)
# print("连通分量：", len(S))
# print("连通分量_one：", number_one)
# for subgraphValue in S:
#     print(len(subgraphValue.nodes()))
# listnodes=[]
# for subgraphValue in S:
#     listnodes.append(len(subgraphValue.nodes()))
# print(listnodes)



# S = [G.subgraph(c).copy() for c in nx.connected_components(G)]
# print(S)









dl = {'city_name': ["陵水黎族自治县",
"三亚",
"乌鲁木齐",
"乌鲁木齐",
"塔城地区",
"塔城地区",
"塔城地区23"
],'city_id_name': ["三亚",
"陵水黎族自治县",
"伊犁哈萨克自治州",
"伊犁哈萨克自治州",
"伊犁哈萨克自治州",
"伊犁哈萨克自治州",
"伊犁哈萨克自治州2"
], 'num': ["0.072079412",
"0.073874935",
"0.063966713",
"0.061093335",
"0.057984026",
"0.052908595",
"0.052908595"
]}

def average_data(df):
    """
    :param df:
    :return:
    """
    # if len(df.values) > 1:
    #     numValue = 0
    #     for i in df.values:
    #         numValue += float(i)
    #     return numValue/2
    # else:
    #     return float(df.values)
# dataframe1 = pd.DataFrame(dl, index=[0,1,2,3,4,5,6])  # 这里注意后加的索引值得跟字典里的值数一样
#
# print(dataframe1)
# print("===========================================")
#
# dataframe4 = dataframe1.groupby(['city_id_name','city_name'])['num'].apply(average_data)
# dataframe4 = dataframe4.reset_index()
# print(dataframe4)
# G.add_node("E")
# - `node_size`: 指定节点的尺寸大小(默认是300，单位未知，就是上图中那么大的点)
# - `node_color`: 指定节点的颜色 (默认是红色，可以用字符串简单标识颜色，例如'r'为红色，'b'为绿色等，具体可查看手册)
# - `node_shape`: 节点的形状（默认是圆形，用字符串'o'标识，具体可查看手册）
# - `alpha`: 透明度 (默认是1.0，不透明，0为完全透明)
# - `width`: 边的宽度 (默认为1.0)
# - `edge_color`: 边的颜色(默认为黑色)
# - `style`: 边的样式(默认为实现，可选： solid|dashed|dotted,dashdot)
# - `with_labels`: 节点是否带标签（默认为True）
# - `font_size`: 节点标签字体大小 (默认为12)
# - `font_color`: 节点标签字体颜色（默认为黑色）

# pos = nx.circular_layout(G)
# nx.draw(G,pos)
# mode_labels = nx.get_node_attributes(G,'desc')
# nx.draw_networkx_nodes(G,pos,label=mode_labels)
# plt.show()
#
# S = [G.subgraph(c).copy() for c in nx.connected_components(G)]
# print(S)



# print(nx.closeness_centrality(G))  #贴近中心度
# n=0
# for val in nx.closeness_centrality(G).values():
#     n += val
# print(n)
# print(nx.betweenness_centrality(G))  #介数中心性
# print(nx.eigenvector_centrality(G))  #特征向量中心性
# print(nx.diameter(G))  #直径



# for xxxx in S:
#     print(xxxx)
#     nx.draw_spectral(xxxx)
# degreeValue= G.degree()
# print(degreeValue)
# for i in degreeValue:
#     print(i[1])

# S = [G.subgraph(c).copy() for c in nx.connected_components(G)]
#
# for i in S:
#     print(i)







# print(nx.average_shortest_path_length(G))
#
# for C in (G.subgraph(c).copy() for c in nx.connected_components(G)):
#     print(nx.average_shortest_path_length(C))

# print(len(nx.minimum_edge_cut(G)))
# allNodes = np.array(G.nodes())
# length  = dict(nx.all_pairs_dijkstra_path_length(G))
# indexColMoveIn =0.073898088
# indexColMoveOut = 0.07026073488
# valueColThree = (indexColMoveIn + indexColMoveOut) / 2

# print(valueColThree)

# sum = 0
# for i in range(G.number_of_nodes()):
#     for j in range(G.number_of_nodes()):
#         sum =sum  + length[allNodes[i]][allNodes[j]]
# print(sum)

# thresholdValue = np.arange(0, 0.25, 0.01)
# print(thresholdValue)


# allNodes = np.array(G.nodes())
# AEC_LastValue = []
# for i in range(0, G.number_of_nodes()):
#     for j in range(i + 1, G.number_of_nodes()):
#         print(allNodes[i], allNodes[j])
#         AEC_EveryValue = nx.edge_connectivity(G, allNodes[i], allNodes[j])
#         AEC_LastValue.append(AEC_EveryValue)
# AEC_LastValue.sort()
# print(AEC_LastValue[0])
nodeList=['舟山', '贵阳', '黄石', '昭通', '焦作', '南通', '丽水', '晋城', '巴中', '阜新', '合肥', '威海', '宿州', '德阳', '白山', '延安', '攀枝花', '佛山', '亳州', '天门', '濮阳', '池州', '漯河', '盐城', '厦门', '丹东', '保山', '贵港', '南昌', '绵阳', '黄冈', '廊坊', '鄂州', '渭南', '宣城', '乐山', '昆明', '淮安', '云浮', '南京', '长治', '防城港', '鞍山', '泸州', '大连', '阳泉', '盘锦', '温州', '赣州', '荆门', '西宁', '湘西土家族苗族自治州', '吉安', '开封', '铜陵', '孝感', '呼和浩特', '佳木斯', '枣庄', '眉山', '遂宁', '武汉', '许昌', '达州', '青岛', '承德', '咸阳', '驻马店', '天水', '苏州', '长春', '黑河', '连云港', '红河哈尼族彝族自治州', '辽阳', '六安', '菏泽', '衡水', '营口', '兴安盟', '岳阳', '黔南布依族苗族自治州', '湘潭', '泉州', '齐齐哈尔', '平顶山', '武威', '宜昌', '滁州', '江门', '临沧', '玉溪', '郴州', '葫芦岛', '沈阳', '商丘', '潜江', '南充', '嘉兴', '东莞', '广安', '恩施土家族苗族自治州', '乌兰察布', '潍坊', '襄阳', '天津', '茂名', '大庆', '邢台', '镇江', '张掖', '河源', '东营', '绥化', '马鞍山', '台州', '抚顺', '柳州', '西双版纳傣族自治州', '西安', '白银', '蚌埠', '揭阳', '宜春', '九江', '邵阳', '阜阳', '四平', '张家口', '湛江', '铁岭', '德宏傣族景颇族自治州', '普洱', '荆州', '伊春', '济宁', '烟台', '珠海', '太原', '本溪', '惠州', '无锡', '双鸭山', '安阳', '运城', '衡阳', '广州', '玉林', '淮北', '凉山彝族自治州', '自贡', '常德', '海南藏族自治州', '长沙', '宁德', '呼伦贝尔', '百色', '新乡', '包头', '甘孜藏族自治州', '朔州', '辽源', '海西蒙古族藏族自治州', '张家界', '重庆', '庆阳', '聊城', '泰州', '上饶', '曲靖', '郑州', '中山', '安顺', '白城', '漳州', '淮南', '桂林', '南宁', '益阳', '济源', '文山壮族苗族自治州', '北海', '抚州', '阳江', '秦皇岛', '梅州', '成都', '德州', '锦州', '安康', '巴彦淖尔', '河池', '汕头', '通化', '龙岩', '梧州', '宜宾', '莆田', '济南', '安庆', '萍乡', '深圳', '日照', '赤峰', '宁波', '平凉', '邯郸', '丽江', '大同', '汕尾', '株洲', '宿迁', '怀化', '钦州', '哈尔滨', '南平', '宝鸡', '鹤岗', '榆林', '通辽', '随州', '泰安', '鹤壁', '朝阳', '资阳', '雅安', '仙桃', '信阳', '楚雄彝族自治州', '潮州', '绍兴', '周口', '常州', '吕梁', '忻州', '景德镇', '三明', '鹰潭', '杭州', '金华', '鄂尔多斯', '衢州', '牡丹江', '陇南', '铜川', '扬州', '临夏回族自治州', '阿坝藏族羌族自治州', '芜湖', '清远', '来宾', '石家庄', '定西', '福州', '黔东南苗族侗族自治州', '广元', '洛阳', '淄博', '临汾', '娄底', '鸡西', '北京', '沧州', '崇左', '海北藏族自治州', '贺州', '湖州', '三门峡', '临沂', '肇庆', '大理白族自治州', '咸宁', '徐州', '内江', '兰州', '唐山', '永州', '黔西南布依族苗族自治州', '韶关', '晋中', '遵义', '松原', '上海', '十堰', '乌海', '金昌', '商洛', '南阳', '六盘水', '汉中', '延边朝鲜族自治州', '锡林郭勒盟', '保定', '新余', '滨州']
listajdia12qwe =['湘西土家族苗族自治州', '红河哈尼族彝族自治州', '黔南布依族苗族自治州', '恩施土家族苗族自治州', '西双版纳傣族自治州', '德宏傣族景颇族自治州', '凉山彝族自治州', '海南藏族自治州', '甘孜藏族自治州', '海西蒙古族藏族自治州', '文山壮族苗族自治州', '楚雄彝族自治州', '临夏回族自治州', '阿坝藏族羌族自治州', '黔东南苗族侗族自治州', '海北藏族自治州', '大理白族自治州', '黔西南布依族苗族自治州', '延边朝鲜族自治州']
# for i in nodeList:
#     if "自治州" in i:
#         listajdia.append(i)
# print(listajdia)
# 01 {'吉林', '毕节', '铜仁'}
# list_city_name=[]
# dataMiga = pd.read_csv("F:\\01大连民族\\百度迁徙爬取和数据\\百度迁徙数据-final\\03将两个In和Out相同行合并_最终数据\\20200503finalData.csv")
# for row in dataMiga.itertuples():
#     city_name = getattr(row, "city_name")
#     city_id_name = getattr(row, "city_id_name")
#     if city_name not in nodeList:
#         list_city_name.append(city_name)
#     if city_id_name not in nodeList:
#         list_city_name.append(city_id_name)
# print(set(list_city_name))

