# -*- coding: utf-8 -*-
"""
#!/usr/bin/env python

@file: generate_csv_file.py
@author: wu hao
@time: 2022/9/26 9:27
@env: 封城数据处理
@desc:
@ref:
"""
import os
import time

import networkx as nx
import pandas as pd
import csv
import datetime
from tqdm import tqdm
#迁徙数据位置
fileNameFront = "F:/百度迁徙数据/比例和指数计算完成后的数据/"
#处理后存储的位置
file_project =  r"F:/封城数据处理/封城数据/石家庄/"

# 石家庄一阶城市
First_order = ["石家庄","北京","衡水","秦皇岛","唐山","廊坊","天津","承德","保定","沧州","邯郸","邢台","张家口"]
# 石家庄二阶城市
Second_order =  ['南京', '广州', '长沙', '邯郸', '深圳', '忻州', '长春', '廊坊', '秦皇岛', '锡林郭勒盟', '杭州', '哈尔滨', '三亚', '聊城', '合肥', '沧州', '西安', '衡水', '沈阳', '葫芦岛', '张家口', '苏州', '呼和浩特', '赤峰', '太原', '周口', '天津', '青岛', '潍坊', '菏泽', '济南', '安阳', '北京', '成都', '大同', '滨州', '乌兰察布', '唐山', '临汾', '晋中', '长治', '德州', '浙江', '重庆', '阳泉', '石家庄', '莱芜', '濮阳', '承德', '邢台', '上海', '郑州', '武汉', '保定']
# 石家庄三阶城市
Third_order =  ['绍兴', '齐齐哈尔', '潍坊', '唐山', '哈尔滨', '大同', '三亚', '天门', '盘锦', '儋州', '平顶山', '湖州', '承德', '南昌', '绥化', '佳木斯', '孝感', '长春', '邵阳', '太原', '玉林', '许昌', '莱芜', '青岛', '晋中', '荆门', '丽水', '泰安', '衡水', '合肥', '长治', '梧州', '烟台', '自贡', '湘潭', '鄂尔多斯', '九江', '辽源', '菏泽', '商丘', '惠州', '连云港', '广西壮族自治区', '三门峡', '汕头', '海口', '天津', '临沂', '浙江', '渭南', '德阳', '常州', '铜仁', '雅安', '乌海', '宜宾', '开封', '揭阳', '苏州', '蚌埠', '邯郸', '伊春', '金华', '宜春', '杭州', '银川', '娄底', '毕节', '随州', '忻州', '黄石', '南通', '枣庄', '萍乡', '辽阳', '朝阳', '吉安', '濮阳', '临汾', '南阳', '株洲', '温州', '毕节地区', '衢州', '南京', '铁岭', '广州', '池州', '西安', '贵港', '鹤岗', '商洛', '韶关', '肇庆', '石家庄', '沧州', '阜阳', '中山', '湛江', '包头', '漯河', '乌兰察布', '阜新', '广元', '东营', '遂宁', '南宁', '巴彦淖尔', '抚顺', '恩施土家族苗族自治州', '郑州', '七台河', '大庆', '廊坊', '六安', '达州', '上饶', '赣州', '日照', '周口', '甘孜藏族自治州', '亳州', '驻马店', '盐城', '松原', '延安', '庆阳', '鹤壁', '嘉兴', '马鞍山', '眉山', '泸州', '芜湖', '镇江', '吕梁', '万宁', '清远', '鞍山', '滁州', '焦作', '益阳', '信阳', '云浮', '长沙', '岳阳', '德州', '运城', '沈阳', '锦州', '淄博', '无锡', '白城', '南充', '舟山', '黄冈', '遵义', '通化', '珠海', '广安', '张家口', '成都', '荆州', '绵阳', '本溪', '郴州', '梅州', '北京', '营口', '贺州', '潜江', '衡阳', '双鸭山', '铜仁地区', '怀化', '平凉', '佛山', '淮南', '咸阳', '阳泉', '内蒙古自治区', '鄂州', '安康', '铜陵', '宿州', '晋城', '巴中', '汉中', '福州', '潮州', '黑河', '仙桃', '常德', '济源', '上海', '茂名', '徐州', '滨州', '攀枝花', '洛阳', '厦门', '延边朝鲜族自治州', '昆明', '黄山', '牡丹江', '吉林', '威海', '呼和浩特', '河源', '湘西土家族苗族自治州', '保定', '东莞', '阳江', '台州', '榆林', '乐山', '内江', '贵阳', '宜昌', '东方', '淮北', '保亭黎族苗族自治县', '凉山彝族自治州', '重庆', '朔州', '兰州', '四平', '宿迁', '葫芦岛', '江门', '陵水黎族自治县', '天水', '资阳', '阿坝藏族羌族自治州', '白山', '丹东', '宝鸡', '济南', '淮安', '泉州', '桂林', '武汉', '琼海', '襄阳', '咸宁', '乐东黎族自治县', '铜川', '锡林郭勒盟', '新乡', '济宁', '邢台', '鸡西', '扬州', '张家界', '秦皇岛', '通辽', '安庆', '深圳', '十堰', '大连', '泰州', '安阳', '赤峰', '宁波', '汕尾', '聊城', '永州', '宣城']
# 石家庄四阶城市
Fourth_order =  ['扬州', '温州', '池州', '锡林郭勒盟', '南平', '杭州', '黑河', '酒泉', '舟山', '嘉兴', '武汉', '信阳', '攀枝花', '毕节', '威海', '随州', '澳门', '楚雄彝族自治州', '株洲', '琼中黎族苗族自治县', '许昌', '玉溪', '永州', '白城', '蚌埠', '天水', '晋中', '宣城', '昆明', '漳州', '葫芦岛', '益阳', '鹰潭', '青岛', '东方', '桂林', '中卫', '铜陵', '佳木斯', '抚顺', '安康', '襄阳', '遵义', '海东', '玉林', '湘潭', '黔西南布依族苗族自治州', '抚州', '大同', '岳阳', '盘锦', '咸阳', '鹤壁', '淮南', '亳州', '湘西土家族苗族自治州', '张家口', '吴忠', '南昌', '吕梁', '鞍山', '马鞍山', '柳州', '成都', '兴安盟', '齐齐哈尔', '泰安', '濮阳', '邯郸', '锦州', '天门', '泸州', '内蒙古自治区', '长春', '贵港', '南阳', '白山', '湖州', '保定', '六盘水', '上饶', '临高', '郴州', '三明', '来宾', '滁州', '巴中', '阿坝藏族羌族自治州', '绥化', '乌兰察布', '呼和浩特', '绵阳', '宿州', '大庆', '惠州', '廊坊', '万宁', '红河哈尼族彝族自治州', '秦皇岛', '丽水', '梅州', '西双版纳傣族自治州', '韶关', '荆州', '烟台', '百色', '澄迈', '河池', '莆田', '白沙黎族自治县', '深圳', '大连', '汕尾', '萍乡', '双鸭山', '呼伦贝尔', '漯河', '五指山', '宁波', '驻马店', '黄冈', '内江', '北京', '沈阳', '达州', '合肥', '白银', '三门峡', '宜春', '通化', '芜湖', '伊春', '张掖', '松原', '澄迈县', '泉州', '南宁', '宜宾', '周口', '阳泉', '十堰', '济南', '衡水', '安庆', '东营', '济宁', '通辽', '常德', '南充', '七台河', '常州', '宜昌', '东莞', '宿迁', '毕节地区', '临沂', '琼海', '儋州', '鄂州', '怀化', '福州', '定西', '鄂尔多斯', '商丘', '乐东黎族自治县', '乌海', '太原', '海口', '曲靖', '淮安', '陇南', '焦作', '新疆维吾尔自治区', '广元', '衡阳', '鸡西', '黄石', '邢台', '临高县', '珠海', '乐山', '巴彦淖尔', '赣州', '荆门', '无锡', '揭阳', '阿拉善盟', '汕头', '临沧', '吉安', '屯昌县', '仙桃', '佛山', '丹东', '九江', '金昌', '云浮', '晋城', '石家庄', '洛阳', '银川', '张家界', '定安', '安阳', '临汾', '南通', '保亭黎族苗族自治县', '淄博', '文山壮族苗族自治州', '新余', '营口', '渭南', '平顶山', '临夏回族自治州', '陵水黎族自治县', '中山', '固原', '西安', '连云港', '徐州', '江门', '聊城', '资阳', '德州', '武威', '淮北', '上海', '遂宁', '阳江', '南京', '自贡', '钦州', '贺州', '济源', '辽阳', '海东地区', '浙江', '潮州', '西宁', '景德镇', '菏泽', '龙岩', '运城', '梧州', '朔州', '郑州', '包头', '四平', '恩施土家族苗族自治州', '三亚', '贵阳', '黔南布依族苗族自治州', '哈尔滨', '安顺', '黔东南苗族侗族自治州', '吉林', '崇左', '河源', '日照', '牡丹江', '延边朝鲜族自治州', '辽源', '眉山', '宝鸡', '苏州', '潍坊', '潜江', '朝阳', '石嘴山', '广州', '娄底', '莱芜', '长治', '邵阳', '承德', '昌江黎族自治县', '枣庄', '西藏自治区', '文昌', '大理白族自治州', '铜仁', '茂名', '凉山彝族自治州', '甘南藏族自治州', '铁岭', '德宏傣族景颇族自治州', '昭通', '阜阳', '阜新', '黄山', '湛江', '广安', '盐城', '延安', '保山', '本溪', '普洱', '庆阳', '孝感', '鹤岗', '肇庆', '甘孜藏族自治州', '台州', '泰州', '定安县', '沧州', '赤峰', '绍兴', '开封', '铜仁地区', '金华', '天津', '商洛', '滨州', '汉中', '兰州', '平凉', '防城港', '广西壮族自治区', '厦门', '宁夏回族自治区', '宁德', '铜川', '唐山', '长沙', '六安', '北海', '镇江', '忻州', '重庆', '衢州', '屯昌', '清远', '雅安', '榆林', '咸宁', '新乡', '丽江', '德阳']
#石家庄五阶城市直接全部包括


 #判断2个字符串字符是否完全一样 顺序可不同
def compare_two_str(a,b):
    if len(a) != len(b):
        return False
    return sorted(a) == sorted(b)

# 日期时间递增 格式yyyymmdd
def getdaylist(beginDate,endDate):
    beginDate = datetime.datetime.strptime(str(beginDate), "%Y%m%d")
    endDate = datetime.datetime.strptime(str(endDate), "%Y%m%d")
    dayList = []
    while beginDate <= endDate:
        dayList.append(datetime.datetime.strftime(beginDate, "%Y%m%d"))
        beginDate += datetime.timedelta(days=+1)
    return dayList




def select_around_city_data(beginTime,endTime,around_city,rank_level):
    """
    属于第一步
    处理直接去掉0.04阈值后in和out的合并
    :param beginTime:
    :param endTime:
    :return:
    """
    dayList = getdaylist(beginTime,endTime)
    # 循环取每一天的值
    for i in tqdm( range(len(dayList)),desc="第一步合并：进度", total=len(dayList)):
        # 迁入数据
        try:
            moveIn = pd.read_csv(fileNameFront+"in\\"+dayList[i]+".csv")
        except Exception as problem:
            print("error打开迁入（in）有问题：", problem)
            continue
        # 迁出数据
        try:
            moveOut = pd.read_csv(fileNameFront+"out\\" + dayList[i] + ".csv")
        except Exception as problem:
            print("error打开迁出（out）有问题：", problem)
            continue

        # 创建处理完的数据csv
        # 表头
        field_order_move_in = ["city_name", 'city_id_name', 'num']
        # 开始写入整理完的数据csv
        path_file_in = file_project+rank_level+"/garbage_self_network/deal_01/in/"
        if not os.path.exists(path_file_in):
            os.makedirs(path_file_in)
        with open(path_file_in + dayList[i] + "_石家庄.csv", 'w',encoding="utf-8", newline='') as csvfile:

            writer = csv.DictWriter(csvfile, field_order_move_in)
            writer.writeheader()
            # move_in 每一行
            for row_in in moveIn.itertuples():
                city_name = getattr(row_in, "city_name")
                city_id_name = getattr(row_in, "city_id_name")
                num = getattr(row_in, "num")
                if num >=0.04:
                    if city_name in around_city and city_id_name in around_city:
                        row = {"city_name": city_name, "city_id_name": city_id_name, "num": num}
                        writer.writerow(row)

            path_file_out = file_project +rank_level+ "/garbage_self_network/deal_01/out/"
            if not os.path.exists(path_file_out):
                os.mkdir(path_file_out)
            with open(path_file_out+ dayList[i] + "_石家庄.csv", 'w',encoding="utf-8", newline='') as csvfile:
                writer = csv.DictWriter(csvfile, field_order_move_in)
                writer.writeheader()
                # move_in 每一行
                for row_out in moveOut.itertuples():
                    city_name = getattr(row_out, "city_name")
                    city_id_name = getattr(row_out, "city_id_name")
                    num = getattr(row_out, "num")
                    if num >= 0.04:
                        if city_name in Second_order and city_id_name in Second_order:
                            row = {"city_name": city_name, "city_id_name": city_id_name, "num": num}
                            writer.writerow(row)

def merge_alone_file(beginTime,endTime,rank_level):
    """
    第二步，合并单独的in里面的内容
    :param beginTime:
    :param endTime:
    :return:
    """
    global moveIn, moveOut
    dayList = getdaylist(beginTime, endTime)
    # 循环取每一天的值
    for i in tqdm(range(len(dayList)), desc="第二步合并：进度", total=len(dayList)):
        # 迁入数据
        try:
            moveIn = pd.read_csv(file_project +rank_level+ "/garbage_self_network/deal_01/in/" + dayList[i] + "_石家庄.csv")
        except Exception as problem:
            print("error打开迁入（in）有问题：", problem)

        # 表头
        field_order_move_in = ["city_name", 'city_id_name', 'num']
        # 开始写入整理完的数据csv
        path_file_in = file_project +rank_level+ "/garbage_self_network/deal_02/in/"
        if not os.path.exists(path_file_in):
            os.makedirs(path_file_in)
        with open(path_file_in + dayList[i] + "_石家庄.csv", 'w', encoding="utf-8", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, field_order_move_in)
            writer.writeheader()
            for row_in in moveIn.itertuples():
                num_in = getattr(row_in, "num")
                city_name = getattr(row_in, "city_name")
                city_id_name = getattr(row_in, "city_id_name")
                listMoveIn = []
                listMoveIn.append(getattr(row_in, "city_name"))
                listMoveIn.append(getattr(row_in, "city_id_name"))
                for row_in_two in moveIn.itertuples():
                    num_out = getattr(row_in_two, "num")
                    listMove_in_two = []
                    listMove_in_two.append(getattr(row_in_two, "city_name"))
                    listMove_in_two.append(getattr(row_in_two, "city_id_name"))
                    # 判断两个列表是否相同 ，来进value值相加除二
                    if compare_two_str(listMoveIn, listMove_in_two):
                        valueColThree = (num_in + num_out) / 2
                        row = {"city_name": city_name, "city_id_name": city_id_name,
                               "num": valueColThree}
                        writer.writerow(row)
        # 迁出数据
        try:
            moveOut = pd.read_csv(file_project +rank_level+ "/garbage_self_network/deal_01/out/" + dayList[i] + "_石家庄.csv")
        except Exception as problem:
            print("error打开迁出（out）有问题：", problem)

        # 创建处理完的数据csv
        # 表头
        field_order_move_in = ["city_name", 'city_id_name', 'num']
        # 开始写入整理完的数据csv
        path_file_in = file_project +rank_level+ "/garbage_self_network/deal_02/out/"
        if not os.path.exists(path_file_in):
            os.makedirs(path_file_in)
        with open(path_file_in + dayList[i] + "_石家庄.csv", 'w', encoding="utf-8", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, field_order_move_in)
            writer.writeheader()
            # move_in 每一行
            for row_out_one in moveOut.itertuples():
                num_in = getattr(row_out_one, "num")
                city_name = getattr(row_out_one, "city_name")
                city_id_name = getattr(row_out_one, "city_id_name")
                listMove_out_one = []
                listMove_out_one.append(getattr(row_out_one, "city_name"))
                listMove_out_one.append(getattr(row_out_one, "city_id_name"))
                for row_out in moveOut.itertuples():
                    num_out = getattr(row_out, "num")
                    listMove_out = []
                    listMove_out.append(getattr(row_out, "city_name"))
                    listMove_out.append(getattr(row_out, "city_id_name"))
                    # 判断两个列表是否相同 ，来进value值相加除二
                    if compare_two_str(listMove_out_one, listMove_out):
                        valueColThree = (num_in + num_out) / 2
                        row = {"city_name": city_name, "city_id_name": city_id_name,
                               "num": valueColThree}
                        writer.writerow(row)


def merge_inAndout_file(beginTime,endTime,rank_level):
    """
    属于第三步 合并in和out里面的重复内容
    :param beginTime:
    :param endTime:
    :return:
    """
    global moveIn, moveOut
    dayList = getdaylist(beginTime,endTime)
    # 循环取每一天的值
    for i in tqdm(range(len(dayList)),desc="第三步合并：进度",total=len(dayList)):
        # 迁入数据
        try:
            moveIn = pd.read_csv(file_project+rank_level+"/garbage_self_network/deal_02/in/"+dayList[i]+"_石家庄.csv")
        except Exception as problem:
            print("error打开迁入（in）有问题：", problem)
        # 迁出数据
        try:
            moveOut = pd.read_csv(file_project+rank_level+"/garbage_self_network/deal_02/out/"+dayList[i]+"_石家庄.csv")
        except Exception as problem:
            print("error打开迁出（out）有问题：", problem)

        # 创建处理完的数据csv
        # 表头
        field_order_move_in = ["city_name", 'city_id_name', 'num']
        # 开始写入整理完的数据csv
        path_file_in = file_project+rank_level+"/garbage_self_network/deal_03/"
        if not os.path.exists(path_file_in):
            os.makedirs(path_file_in)
        with open(path_file_in+ dayList[i] + "_石家庄.csv", 'w',encoding="utf-8", newline='') as csvfile:

            writer = csv.DictWriter(csvfile, field_order_move_in)
            writer.writeheader()
            # move_in 每一行
            for row_in in moveIn.itertuples():
                num_in = getattr(row_in, "num")
                city_name = getattr(row_in, "city_name")
                city_id_name = getattr(row_in, "city_id_name")
                listMoveIn = []
                listMoveIn.append(getattr(row_in, "city_name"))
                listMoveIn.append(getattr(row_in, "city_id_name"))
                for row_out in moveOut.itertuples():
                    num_out = getattr(row_out, "num")
                    listMove_out = []
                    listMove_out.append(getattr(row_out, "city_name"))
                    listMove_out.append(getattr(row_out, "city_id_name"))
                    # 判断两个列表是否相同 ，来进value值相加除二
                    if compare_two_str(listMoveIn, listMove_out):
                        valueColThree = (num_in + num_out) / 2
                        row = {"city_name": city_name, "city_id_name": city_id_name,
                               "num": valueColThree}
                        writer.writerow(row)


if __name__ == '__main__':
    # select_around_city_data(20210101,20210508,Fourth_order,"石家庄四阶")
    merge_alone_file(20210101,20210508,"石家庄四阶")
    merge_inAndout_file(20210101,20210508,"石家庄四阶")
