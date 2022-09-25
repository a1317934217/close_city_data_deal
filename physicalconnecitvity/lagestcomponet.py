#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/11/21 9:34
# @Author  : wuhao
# @Email   : guess?????
# @File    : lagestcomponet.py
import time
import numpy as np
import networkx as nx
import pandas as pd
import csv
import datetime
# 根据路径画图
from numpy import array
from pandas.core.frame import DataFrame

def drawpicture(filePath):
    """
    输入文件路径最后绘制成图G
    """
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


# filePath = "F:\\01大连民族\\百度迁徙爬取和数据\\百度迁徙数据-final\\20200201physical.csv"
# # dataNumber = pd.read_csv("F:\\01大连民族\\百度迁徙爬取和数据\\百度迁徙数据-final\\20200201physical.csv")
# G = drawpicture(filePath)
# # 最大联通组件
# largest_cc = max(nx.connected_components(G), key=len)
# print(largest_cc)
# print(len(largest_cc))
#
#
# largest_week = nx.number_weakly_connected_components(G)
# print(largest_week)
lastname=['舟山', '贵阳', '黄石', '昭通', '焦作', '南通', '丽水', '晋城', '巴中', '阜新', '合肥', '威海', '宿州', '德阳', '白山', '延安', '攀枝花', '佛山', '亳州', '天门', '濮阳', '池州', '漯河', '盐城', '厦门', '丹东', '保山', '贵港', '南昌', '绵阳', '黄冈', '廊坊', '鄂州', '渭南', '宣城', '乐山', '昆明', '淮安', '云浮', '南京', '长治', '防城港', '鞍山', '泸州', '大连', '阳泉', '盘锦', '温州', '赣州', '荆门', '西宁', '湘西土家族苗族自治州', '吉安', '开封', '铜陵', '孝感', '呼和浩特', '佳木斯', '枣庄', '眉山', '遂宁', '武汉', '许昌', '达州', '青岛', '承德', '咸阳', '驻马店', '天水', '苏州', '长春', '黑河', '连云港', '红河哈尼族彝族自治州', '辽阳', '六安', '菏泽', '衡水', '营口', '兴安盟', '岳阳', '黔南布依族苗族自治州', '湘潭', '泉州', '齐齐哈尔', '平顶山', '武威', '宜昌', '滁州', '江门', '临沧', '玉溪', '郴州', '葫芦岛', '沈阳', '商丘', '潜江', '南充', '嘉兴', '东莞', '广安', '恩施土家族苗族自治州', '乌兰察布', '潍坊', '襄阳', '天津', '茂名', '大庆', '邢台', '镇江', '张掖', '河源', '东营', '绥化', '马鞍山', '台州', '抚顺', '柳州', '西双版纳傣族自治州', '西安', '白银', '蚌埠', '揭阳', '宜春', '九江', '邵阳', '阜阳', '四平', '张家口', '湛江', '铁岭', '德宏傣族景颇族自治州', '普洱', '荆州', '伊春', '济宁', '烟台', '珠海', '太原', '本溪', '惠州', '无锡', '双鸭山', '安阳', '运城', '衡阳', '广州', '玉林', '淮北', '凉山彝族自治州', '自贡', '常德', '海南藏族自治州', '长沙', '宁德', '呼伦贝尔', '百色', '新乡', '包头', '甘孜藏族自治州', '朔州', '辽源', '海西蒙古族藏族自治州', '张家界', '重庆', '庆阳', '聊城', '泰州', '上饶', '曲靖', '郑州', '中山', '安顺', '白城', '漳州', '淮南', '桂林', '南宁', '益阳', '济源', '文山壮族苗族自治州', '北海', '抚州', '阳江', '秦皇岛', '梅州', '成都', '德州', '锦州', '安康', '巴彦淖尔', '河池', '汕头', '通化', '龙岩', '梧州', '宜宾', '莆田', '济南', '安庆', '萍乡', '深圳', '日照', '赤峰', '宁波', '平凉', '邯郸', '丽江', '大同', '汕尾', '株洲', '宿迁', '怀化', '钦州', '哈尔滨', '南平', '宝鸡', '鹤岗', '榆林', '通辽', '随州', '泰安', '鹤壁', '朝阳', '资阳', '雅安', '仙桃', '信阳', '楚雄彝族自治州', '潮州', '绍兴', '周口', '常州', '吕梁', '忻州', '景德镇', '三明', '鹰潭', '杭州', '金华', '鄂尔多斯', '衢州', '牡丹江', '陇南', '铜川', '扬州', '临夏回族自治州', '阿坝藏族羌族自治州', '芜湖', '清远', '来宾', '石家庄', '定西', '福州', '黔东南苗族侗族自治州', '广元', '洛阳', '淄博', '临汾', '娄底', '鸡西', '北京', '沧州', '崇左', '海北藏族自治州', '贺州', '湖州', '三门峡', '临沂', '肇庆', '大理白族自治州', '咸宁', '徐州', '内江', '兰州', '唐山', '永州', '黔西南布依族苗族自治州', '韶关', '晋中', '遵义', '松原', '上海', '十堰', '乌海', '金昌', '商洛', '南阳', '六盘水', '汉中', '延边朝鲜族自治州', '锡林郭勒盟', '保定', '新余', '滨州']

dataNumber = pd.read_csv("D:\\04python project\\01-爬虫-爬取百度迁徙数据\\qianxi\\ChinaAreaCodes.csv")
cityname = dataNumber[['cityName']]
# print(cityname)
# lastnamevity = DataFrame(lastname)
# lastnamevity.columns = ['cityName']
# print()  #以数组形式打出来方便看
# print(DataFrame(cityname),len(cityname))  #以数组形式打出来方便看
# print(DataFrame(lastnamevity),len(lastname))  #以数组形式打出来方便看

# 取差集(从df1中过滤df1在df2中存在的行)：
# lastnamevity = lastnamevity.append(cityname)
# lastnamevity = lastnamevity.append(cityname)
# lastnamevity = lastnamevity.drop_duplicates(subset=['cityName'],keep=False)
# lastnamevity = lastnamevity.reset_index(drop=True)
# print(type(cityname),len(cityname))
# print(cityname)

listCIty = []
for i in range(len(cityname)):
    clonae = cityname.loc[i]
    listCIty.append(clonae[0])
# print(listCIty)

# b中有而a中没有的
listNeedDel =  list(set(listCIty).difference(set(lastname)))
print(listNeedDel)

# for i in cityname:
#     print(i)
# print(np.asarray(cityname))