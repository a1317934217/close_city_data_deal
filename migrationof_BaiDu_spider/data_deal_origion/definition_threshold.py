#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/2 17:17
# @Author  : wuhao
# @Email   : guess?????
# @File    : definition_threshold.py
import collections
import datetime
import csv
import time
from filecmp import cmp
import operator
import networkx as nx
import pandas as pd
import numpy as np
import unittest

from tqdm import tqdm

all_cityName = ['北京', '天津', '兴安盟', '定安', '屯昌', '澄迈', '临高', '海东地区', '香港', '澳门', '昌都地区', '山南地区', '日喀则地区', '那曲地区', '林芝地区', '吐鲁番地区', '铜仁地区', '毕节地区', '广西壮族自治区', '内蒙古自治区', '宁夏回族自治区', '新疆维吾尔自治区', '西藏自治区', '石家庄', '唐山', '秦皇岛', '邯郸', '邢台', '保定', '张家口', '承德', '沧州', '廊坊', '衡水', '太原', '大同', '阳泉', '长治', '晋城', '朔州', '晋中', '运城', '忻州', '临汾', '吕梁', '呼和浩特', '包头', '乌海', '赤峰', '通辽', '鄂尔多斯', '呼伦贝尔', '巴彦淖尔', '乌兰察布', '沈阳', '大连', '鞍山', '抚顺', '本溪', '丹东', '锦州', '营口', '阜新', '辽阳', '盘锦', '铁岭', '朝阳', '葫芦岛', '长春', '吉林', '四平', '辽源', '通化', '白山', '松原', '白城', '哈尔滨', '齐齐哈尔', '鸡西', '鹤岗', '双鸭山', '大庆', '伊春', '佳木斯', '七台河', '牡丹江', '黑河', '绥化', '上海', '南京', '无锡', '徐州', '常州', '苏州', '南通', '连云港', '淮安', '盐城', '扬州', '镇江', '泰州', '宿迁', '浙江', '杭州', '宁波', '温州', '嘉兴', '湖州', '绍兴', '金华', '衢州', '舟山', '台州', '丽水', '合肥', '芜湖', '蚌埠', '淮南', '马鞍山', '淮北', '铜陵', '安庆', '黄山', '滁州', '阜阳', '宿州', '六安', '亳州', '池州', '宣城', '福州', '厦门', '莆田', '三明', '泉州', '漳州', '南平', '龙岩', '宁德', '南昌', '景德镇', '萍乡', '九江', '新余', '鹰潭', '赣州', '吉安', '宜春', '抚州', '上饶', '济南', '莱芜', '青岛', '淄博', '枣庄', '东营', '烟台', '潍坊', '济宁', '泰安', '威海', '日照', '临沂', '德州', '聊城', '滨州', '菏泽', '郑州', '开封', '洛阳', '平顶山', '安阳', '鹤壁', '新乡', '焦作', '濮阳', '许昌', '漯河', '三门峡', '南阳', '商丘', '信阳', '周口', '驻马店', '武汉', '黄石', '十堰', '宜昌', '襄阳', '鄂州', '荆门', '孝感', '荆州', '黄冈', '咸宁', '随州', '仙桃', '潜江', '天门', '长沙', '株洲', '湘潭', '衡阳', '邵阳', '岳阳', '常德', '张家界', '益阳', '郴州', '永州', '怀化', '娄底', '广州', '韶关', '深圳', '珠海', '汕头', '佛山', '江门', '湛江', '茂名', '肇庆', '惠州', '梅州', '汕尾', '河源', '阳江', '清远', '东莞', '济源', '中山', '潮州', '揭阳', '云浮', '南宁', '柳州', '桂林', '梧州', '北海', '防城港', '钦州', '贵港', '玉林', '百色', '贺州', '河池', '来宾', '崇左', '海口', '三亚', '三亚', '五指山', '琼海', '儋州', '文昌', '万宁', '东方', '重庆', '成都', '自贡', '攀枝花', '泸州', '德阳', '绵阳', '广元', '遂宁', '内江', '乐山', '南充', '眉山', '宜宾', '广安', '达州', '雅安', '巴中', '资阳', '贵阳', '六盘水', '遵义', '安顺', '昆明', '曲靖', '玉溪', '保山', '昭通', '丽江', '临沧', '普洱', '拉萨', '西安', '铜川', '宝鸡', '咸阳', '渭南', '延安', '汉中', '榆林', '安康', '商洛', '兰州', '嘉峪关', '金昌', '白银', '天水', '武威', '张掖', '平凉', '酒泉', '庆阳', '定西', '陇南', '西宁', '银川', '石嘴山', '吴忠', '固原', '中卫', '乌鲁木齐', '克拉玛依', '石河子', '阿拉尔', '图木舒克', '五家渠', '北屯', '铁门关', '双河', '可克达拉', '昆玉', '恩施土家族苗族自治州', '延边朝鲜族自治州', '神农架林区', '湘西土家族苗族自治州', '大兴安岭地区', '白沙黎族自治县', '昌江黎族自治县', '乐东黎族自治县', '陵水黎族自治县', '保亭黎族苗族自治县', '琼中黎族苗族自治县', '阿坝藏族羌族自治州', '甘孜藏族自治州', '凉山彝族自治州', '黔西南布依族苗族自治州', '黔东南苗族侗族自治州', '黔南布依族苗族自治州', '楚雄彝族自治州', '红河哈尼族彝族自治州', '文山壮族苗族自治州', '西双版纳傣族自治州', '大理白族自治州', '德宏傣族景颇族自治州', '怒江傈僳族自治州', '迪庆藏族自治州', '阿里地区', '临夏回族自治州', '甘南藏族自治州', '海北藏族自治州', '黄南藏族自治州', '海南藏族自治州', '果洛藏族自治州', '玉树藏族自治州', '海西蒙古族藏族自治州', '昌吉回族自治州', '博尔塔拉蒙古自治州', '巴音郭楞蒙古自治州', '哈密地区', '阿克苏地区', '克孜勒苏柯尔克孜自治州', '伊犁哈萨克自治州', '喀什地区', '和田地区', '塔城地区', '阿勒泰地区', '锡林郭勒盟', '阿拉善盟']

moveIn = pd.read_csv("F:\\01大连民族\\百度迁徙爬取和数据\\百度迁徙数据-final\\in\\20200101.csv")

# def get_threshold_value():
#     field_order_move_in = ["city_name", "city_id_name", "num"]
#     with open("D:\\04python project\\01-爬虫-爬取百度迁徙数据\\migrationof_BaiDu_spider\\data_deal_origion\\20200101_merge.csv", 'w', encoding="utf-8",
#               newline='') as csvfile:
#         writer = csv.DictWriter(csvfile, field_order_move_in)
#         writer.writeheader()
#         for row_in in moveIn.itertuples():
#             Index_in = getattr(row_in, "Index")
#             in_list =[]
#             city_name_in = getattr(row_in, "city_name")
#             city_id_name_in = getattr(row_in, "city_id_name")
#             num_in = getattr(row_in, "num")
#             num_in = getattr(row_in, "index")
#             in_list.append(city_name_in)
#             in_list.append(city_id_name_in)
#             print("in 的进度",Index_in)
#             if  collections.Counter(in_list) ==  collections.Counter(out_list):
#                 row = {"city_name": city_name_in, "city_id_name": city_id_name_in,"num":num_out+num_out /2}
#                 writer.writerow(row)
#                 break

def get_number_largest_connect():
    data_Deal = pd.read_csv("D:\\04python project\\01-爬虫-爬取百度迁徙数据\migrationof_BaiDu_spider\data_deal_origion\\20200101_merge.csv")
    yuzhi_list = [0.0, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.07, 0.075,
                  0.08, 0.085, 0.09, 0.095, 0.1, 0.105, 0.11, 0.115, 0.12, 0.125, 0.13, 0.135, 0.14, 0.145, 0.15, 0.155,
                  0.16, 0.165, 0.17, 0.17500000000000002, 0.18, 0.185, 0.19, 0.195, 0.2, 0.20500000000000002, 0.21,
                  0.215, 0.22, 0.225, 0.23, 0.23500000000000001, 0.24, 0.245, 0.25]
    size_of_the_largest_connected_component =[]
    number_weakly_connected_component_list=[]
    for threshold  in yuzhi_list:
        G_largest_compont = nx.Graph()
        G_weakly_compont = nx.DiGraph()
        for row in data_Deal.itertuples():
            # Index = getattr(row, "Index")
            city_name = getattr(row, "city_name")
            city_id_name = getattr(row, "city_id_name")
            num = getattr(row, "num")
            if num >=  threshold:
                G_largest_compont.add_edges_from([(city_name, city_id_name)])
                G_weakly_compont.add_edges_from([(city_name, city_id_name)])
        number_weakly_connected_component_list.append(nx.number_weakly_connected_components(G_weakly_compont))
        Gc = max(nx.connected_components(G_largest_compont), key=len)  # 最大连通子图
        ret_list = list(set(Gc) ^ set(all_cityName))
        print("最大组件城市名称：",threshold,len(Gc),Gc,"差集================================================================================:",ret_list)
        size_of_the_largest_connected_component.append(len(Gc))
    return size_of_the_largest_connected_component,number_weakly_connected_component_list

print(get_number_largest_connect())

#0.04  288城市 (最后确定)
#需要删除的城市
# deal_city = ['海北藏族自治州', '天水', '阿克苏地区', '澳门', '黄南藏族自治州', '山南地区', '陵水黎族自治县', '临夏回族自治州', '新疆维吾尔自治区', '锡林郭勒盟', '果洛藏族自治州', '鸡西', '武威', '嘉峪关', '乐东黎族自治县', '昌都地区', '西宁', '陇南', '儋州', '塔城地区', '林芝地区', '西藏自治区', '伊春', '白沙黎族自治县', '北屯', '阿里地区', '海西蒙古族藏族自治州', '图木舒克', '黑河', '克孜勒苏柯尔克孜自治州', '神农架林区', '大兴安岭地区', '巴音郭楞蒙古自治州', '内蒙古自治区', '思茅', '甘南藏族自治州', '怒江傈僳族自治州', '襄樊', '三亚', '乌鲁木齐', '宁夏回族自治区', '和田地区', '博尔塔拉蒙古自治州', '铜仁地区', '吐鲁番地区', '毕节地区', '黄山', '酒泉', '五家渠', '张掖', '七台河', '可克达拉', '哈密地区', '双河', '东方', '石河子', '定西', '白银', '定安', '金昌', '澄迈', '五指山', '铁门关', '毕节', '临沧', '浙江', '阿勒泰地区', '屯昌', '海口', '文昌', '海南藏族自治州', '伊犁哈萨克自治州', '拉萨', '莱芜', '昆玉', '铜仁', '玉树藏族自治州', '日喀则地区', '阿拉尔', '万宁', '海东地区', '喀什地区', '昌吉回族自治州', '平凉', '白山', '琼海', '那曲地区', '临高', '昌江黎族自治县', '克拉玛依', '广西壮族自治区', '保亭黎族苗族自治县', '琼中黎族苗族自治县']

#0.055  295个城市  删除87个城市
deal_city = ['林芝地区', '图木舒克', '阿里地区', '海西蒙古族藏族自治州', '克孜勒苏柯尔克孜自治州', '陇南', '喀什地区', '塔城地区', '五指山', '乐东黎族自治县', '临夏回族自治州', '七台河', '甘南藏族自治州', '那曲地区', '果洛藏族自治州', '海南藏族自治州', '山南地区', '陵水黎族自治县', '可克达拉', '阿克苏地区', '石河子', '广西壮族自治区', '昆玉', '琼海', '白银', '北屯', '万宁', '海东地区', '酒泉', '宁夏回族自治区', '金昌', '临高', '五家渠', '伊春', '阿勒泰地区', '鸡西', '玉树藏族自治州', '天水', '内蒙古自治区', '张掖', '昌都地区', '伊犁哈萨克自治州', '东方', '定安', '保亭黎族苗族自治县', '新疆维吾尔自治区', '昌吉回族自治州', '阿拉尔', '西藏自治区', '昌江黎族自治县', '武威', '白山', '临沧', '儋州', '巴音郭楞蒙古自治州', '西宁', '文昌', '思茅', '日喀则地区', '毕节', '襄樊', '嘉峪关', '吐鲁番地区', '黄南藏族自治州', '铜仁地区', '平凉', '神农架林区', '博尔塔拉蒙古自治州', '铜仁', '定西', '克拉玛依', '哈密地区', '海北藏族自治州', '三亚', '怒江傈僳族自治州', '屯昌', '双河', '铁门关', '澳门', '澄迈', '浙江', '和田地区', '琼中黎族苗族自治县', '白沙黎族自治县', '莱芜', '毕节地区', '大兴安岭地区']
deal_city_one  =['鸡西', '昆玉', '平凉', '定安', '兰州', '林芝地区', '白山', '白银', '昌吉回族自治州', '和田地区', '武威', '张掖', '万宁', '怒江傈僳族自治州', '陵水黎族自治县', '哈密地区', '巴音郭楞蒙古自治州', '铜仁', '海口', '喀什地区', '广西壮族自治区', '文昌', '浙江', '阿勒泰地区', '白沙黎族自治县', '内蒙古自治区', '黄南藏族自治州', '海北藏族自治州', '昌都地区', '东方', '毕节地区', '石河子', '昌江黎族自治县', '天水', '海南藏族自治州', '伊犁哈萨克自治州', '金昌', '双河', '那曲地区', '果洛藏族自治州', '西藏自治区', '海东地区', '北屯', '三亚', '琼中黎族苗族自治县', '乐东黎族自治县', '吐鲁番地区', '玉树藏族自治州', '儋州', '可克达拉', '铁门关', '阿拉尔', '澄迈', '日喀则地区', '铜仁地区', '伊春', '海西蒙古族藏族自治州', '山南地区', '嘉峪关', '莱芜', '临高', '毕节', '陇南', '阿里地区', '五家渠', '克拉玛依', '临夏回族自治州', '新疆维吾尔自治区', '乌鲁木齐', '博尔塔拉蒙古自治州', '澳门', '宁夏回族自治区', '图木舒克', '大兴安岭地区', '阿克苏地区', '神农架林区', '琼海', '酒泉', '保亭黎族苗族自治县', '屯昌', '定西', '塔城地区', '思茅', '克孜勒苏柯尔克孜自治州', '西宁', '临沧', '七台河', '五指山', '拉萨', '甘南藏族自治州', '襄樊']
# ret_list = list(set(deal_city) ^ set(all_cityName))
# print(ret_list)
print(len(deal_city))
print(len(deal_city_one))
# print(len(all_cityName))
# print(len(all_cityName)-len(deal_city))
def compare_two_str(a,b):
    if len(a) != len(b):
        return False
    return sorted(a) == sorted(b)


def merge_in_out_2021():
    """
    合并2021年的整合数据
    :return:
    """

    # 创建处理完的数据csv
    # 表头
    field_order_move_in = ["city_name", 'city_id_name', 'num']
    # 开始写入整理完的数据csv

    move_in_file = "F:\\01大连民族\\百度迁徙爬取和数据\\百度迁徙数据更新_经常运行\\比例和指数计算完成后的数据\\in\\20210101.csv"
    move_out_file = "F:\\01大连民族\\百度迁徙爬取和数据\\百度迁徙数据更新_经常运行\\比例和指数计算完成后的数据\\out\\20210101.csv"
    move_in_data = pd.read_csv(move_in_file)
    move_out_data = pd.read_csv(move_out_file)
    with open("D:\\04python project\\01-爬虫-爬取百度迁徙数据\migrationof_BaiDu_spider\data_deal_origion\\20210101_merge.csv", 'w',
              encoding="utf-8", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, field_order_move_in)
        writer.writeheader()
        for row_in in move_in_data.iterrows():
            city_name_one = row_in[1]["city_name"]
            city_name_two = row_in[1]["city_id_name"]
            value_one = row_in[1]["num"]
            compare_str_one = city_name_two+","+city_name_one
            print(compare_str_one)
            for row_out in tqdm(move_out_data.iterrows()):
                city_name_three = row_out[1]["city_name"]
                city_name_four = row_out[1]["city_id_name"]
                value_two = row_out[1]["num"]
                compare_str_two = city_name_three + "," + city_name_four

                if compare_str_one == compare_str_two:
                    row = {"city_name": city_name_three, "city_id_name": city_name_four, "num": float(value_one)+float(value_two)}
                    writer.writerow(row)
                    break


def deal_merge_data_onefile():
    """
    将in和out合并完的数据继续进行合并
    :return:
    """
     # 表头
    field_order_move_in = ["city_name", 'city_id_name', 'num']
    # 开始写入整理完的数据csv
    need_deal_file_one = pd.read_csv("D:\\04python project\\01-爬虫-爬取百度迁徙数据\migrationof_BaiDu_spider\data_deal_origion\\20210101_merge.csv")
    need_deal_file_two = pd.read_csv("D:\\04python project\\01-爬虫-爬取百度迁徙数据\migrationof_BaiDu_spider\data_deal_origion\\20210101_merge.csv")

    with open("D:\\04python project\\01-爬虫-爬取百度迁徙数据\migrationof_BaiDu_spider\data_deal_origion\\20210101_finall.csv", 'w',
                  encoding="utf-8", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, field_order_move_in)
        writer.writeheader()
        for row_one in tqdm(need_deal_file_one.iterrows(),total=len(need_deal_file_one)):
            list_a=[]
            city_name_one = row_one[1]["city_name"]
            city_name_two = row_one[1]["city_id_name"]
            value_one = row_one[1]["num"]
            list_a.append(city_name_one)
            list_a.append(city_name_two)
            for row_two in need_deal_file_two.iterrows():
                list_b = []
                city_name_three = row_two[1]["city_name"]
                city_name_four = row_two[1]["city_id_name"]
                value_two = row_two[1]["num"]
                list_b.append(city_name_three)
                list_b.append(city_name_four)
                if compare_two_str(list_a,list_b):
                    valueColThree = (float(value_one) + float(value_two)) / 2
                    row = {"city_name": city_name_one, "city_id_name": city_name_two, "num": valueColThree}
                    writer.writerow(row)
                    break




