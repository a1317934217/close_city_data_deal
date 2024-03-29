# coding:utf-8
"""
@file: caculate_down_Anddraw_pic.py
@author: wu hao
@time: 2023/5/5 14:11
@env: 封城数据处理
@desc:
@ref:
"""
import io

from PIL import Image
from numpy import array

# coding:utf-8
"""
@file: close_city_caculate_indicator.py
@author: wu hao
@time: 2022/9/27 7:53
@env: 封城数据处理
@desc:
@ref:
"""

import datetime
from math import e
from math import log

# coding=utf-8
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter, MaxNLocator
# 根据路径画图
from sklearn.preprocessing import MinMaxScaler
from tqdm import tqdm


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

#西安 封城时间 20211223 20220115  比较时间2021/12/09 -2022/1/31(接近春节) 阈值选取为0.08 确定！
#石家庄封城前(20210101)   石家庄封城时(20210114)    石家庄封城后(20210301)

#14个
First_order_xian =  ['铜川', '渭南', '成都', '宝鸡', '咸阳', '延安', '商洛', '榆林', '汉中', '庆阳', '北京', '安康', '西安']
#55个
Second_order_xian =  ['雅安', '凉山彝族自治州', '吕梁', '石家庄', '济南', '唐山', '北京', '宜宾', '成都', '资阳', '达州', '安康', '廊坊', '邯郸', '秦皇岛', '延安', '阿坝藏族羌族自治州', '广安', '汉中', '庆阳', '咸阳', '鄂尔多斯', '渭南', '广元', '张家口', '衡水', '榆林', '泸州', '宝鸡', '内江', '南充', '眉山', '商洛', '铜川', '沧州', '上海', '巴中', '武汉', '承德', '重庆', '遂宁', '绵阳', '乐山', '攀枝花', '自贡', '深圳', '郑州', '甘孜藏族自治州', '西安', '德阳', '忻州', '保定', '天津', '运城', '莱芜']
#144个
Third_order_xian =  ['唐山', '天门', '苏州', '许昌', '黄冈', '宝鸡', '商洛', '临汾', '常州', '广元', '焦作', '太原', '咸宁', '昭通', '庆阳', '铜仁', '咸阳', '榆林', '朔州', '洛阳', '西安', '保定', '聊城', '忻州', '吕梁', '仙桃', '遂宁', '雅安', '铜仁地区', '郑州', '梅州', '德阳', '鄂尔多斯', '汉中', '驻马店', '德州', '巴彦淖尔', '襄阳', '濮阳', '承德', '乌海', '菏泽', '眉山', '清远', '汕尾', '潍坊', '遵义', '韶关', '黄石', '巴中', '鹤壁', '邢台', '泸州', '合肥', '运城', '攀枝花', '随州', '淄博', '商丘', '广州', '宜宾', '中山', '上海', '泰州', '揭阳', '南充', '荆门', '三门峡', '天津', '枣庄', '漯河', '青岛', '无锡', '惠州', '湛江', '潜江', '张家口', '莱芜', '汕头', '临沂', '延安', '泰安', '铜川', '茂名', '达州', '贵阳', '乐山', '开封', '邯郸', '长沙', '廊坊', '甘孜藏族自治州', '绵阳', '安康', '湖州', '赣州', '孝感', '秦皇岛', '石家庄', '自贡', '江门', '荆州', '盐城', '舟山', '沧州', '河源', '成都', '十堰', '周口', '内江', '宜昌', '凉山彝族自治州', '滨州', '呼和浩特', '济南', '东营', '北京', '南通', '鄂州', '安阳', '恩施土家族苗族自治州', '阿坝藏族羌族自治州', '济宁', '南京', '渭南', '南阳', '包头', '宁波', '衡水', '资阳', '佛山', '深圳', '信阳', '珠海', '晋中', '武汉', '广安', '烟台', '重庆', '嘉兴', '东莞', '杭州', '平顶山', '新乡']
#212个
Fourth_order_xian =  ['徐州', '廊坊', '亳州', '上海', '泰州', '鄂尔多斯', '合肥', '黔南布依族苗族自治州', '衡阳', '潜江', '怀化', '周口', '杭州', '洛阳', '邯郸', '贵港', '南充', '驻马店', '遂宁', '淄博', '鹤壁', '长沙', '渭南', '阿坝藏族羌族自治州', '重庆', '镇江', '安顺', '自贡', '石家庄', '南京', '汉中', '菏泽', '达州', '铜陵', '濮阳', '沧州', '聊城', '资阳', '许昌', '南通', '安阳', '巴中', '宿州', '甘孜藏族自治州', '常德', '永州', '东莞', '珠海', '信阳', '阳江', '襄阳', '承德', '攀枝花', '贵阳', '济宁', '三门峡', '咸宁', '平顶山', '黔东南苗族侗族自治州', '台州', '德阳', '张家界', '晋城', '成都', '天津', '荆门', '淮安', '十堰', '咸阳', '张家口', '铜仁', '烟台', '衢州', '太原', '枣庄', '延安', '呼和浩特', '湘潭', '焦作', '吕梁', '金华', '盐城', '佛山', '运城', '池州', '韶关', '玉林', '榆林', '德州', '绍兴', '邢台', '九江', '恩施土家族苗族自治州', '凉山彝族自治州', '天门', '滨州', '舟山', '新乡', '广元', '宿迁', '萍乡', '马鞍山', '郑州', '肇庆', '武汉', '汕头', '宝鸡', '扬州', '庆阳', '阳泉', '衡水', '秦皇岛', '无锡', '巴彦淖尔', '黄冈', '包头', '淮南', '六盘水', '六安', '大同', '滁州', '内江', '荆州', '乌海', '汕尾', '泸州', '铜川', '眉山', '威海', '南昌', '宜昌', '朔州', '阿拉善盟', '泰安', '江门', '连云港', '东营', '安庆', '茂名', '广安', '吉安', '宁波', '随州', '赣州', '湖州', '阜阳', '唐山', '黄石', '晋中', '中山', '潍坊', '济源', '黄山', '温州', '常州', '绵阳', '西安', '乐山', '昆明', '湛江', '铜仁地区', '湘西土家族苗族自治州', '惠州', '开封', '临汾', '鄂州', '澳门', '苏州', '郴州', '清远', '娄底', '保定', '商丘', '日照', '忻州', '安康', '长治', '梧州', '漯河', '青岛', '云浮', '孝感', '济南', '梅州', '株洲', '雅安', '宜宾', '揭阳', '仙桃', '益阳', '宜春', '河源', '黔西南布依族苗族自治州', '嘉兴', '毕节地区', '毕节', '乌兰察布', '深圳', '遵义', '北京', '昭通', '临沂', '芜湖', '宣城', '南阳', '邵阳', '商洛', '广州', '潮州', '岳阳', '莱芜', '蚌埠']
#241个
five_order_xian = ['娄底', '烟台', '广安', '邢台', '上饶', '惠州', '温州', '安庆', '宁德', '荆州', '阳江', '北京', '承德', '天门', '贵港', '凉山彝族自治州', '达州', '广州', '北海', '阿坝藏族羌族自治州', '青岛', '大同', '鄂尔多斯', '驻马店', '池州', '济南', '赣州', '扬州', '内江', '毕节', '许昌', '襄阳', '湖州', '包头', '泸州', '上海', '茂名', '鹤壁', '眉山', '苏州', '澳门', '聊城', '柳州', '六盘水', '晋城', '乌兰察布', '武汉', '金华', '无锡', '安康', '雅安', '铜川', '枣庄', '黔南布依族苗族自治州', '来宾', '天津', '云浮', '南京', '长沙', '深圳', '宁波', '舟山', '盐城', '莱芜', '自贡', '乌海', '曲靖', '六安', '保山', '咸阳', '呼和浩特', '东莞', '潍坊', '南昌', '阿拉善盟', '丽江', '汕尾', '遂宁', '玉林', '怀化', '淮安', '成都', '红河哈尼族彝族自治州', '崇左', '常州', '福州', '秦皇岛', '贵阳', '吕梁', '鹰潭', '毕节地区', '马鞍山', '濮阳', '长治', '大理白族自治州', '宣城', '安顺', '防城港', '江门', '湛江', '肇庆', '泰州', '铜仁地区', '新余', '株洲', '阜阳', '漯河', '临沂', '文山壮族苗族自治州', '仙桃', '中山', '河池', '杭州', '蚌埠', '昭通', '韶关', '石家庄', '恩施土家族苗族自治州', '衡水', '宝鸡', '嘉兴', '绍兴', '宜昌', '益阳', '朔州', '昆明', '河源', '郑州', '郴州', '张家界', '资阳', '合肥', '黔西南布依族苗族自治州', '济宁', '玉溪', '运城', '邯郸', '徐州', '宜春', '清远', '十堰', '南宁', '丽水', '桂林', '黄山', '镇江', '铜仁', '咸宁', '黄冈', '芜湖', '潮州', '商洛', '百色', '湘潭', '周口', '安阳', '楚雄彝族自治州', '攀枝花', '永州', '汉中', '滁州', '衡阳', '巴中', '邵阳', '常德', '西安', '德州', '抚州', '九江', '洛阳', '景德镇', '开封', '新乡', '鄂州', '菏泽', '巴彦淖尔', '张家口', '晋中', '宜宾', '南阳', '荆门', '普洱', '乐山', '重庆', '钦州', '湘西土家族苗族自治州', '西双版纳傣族自治州', '平顶山', '黄石', '宿州', '淄博', '三门峡', '甘孜藏族自治州', '保定', '亳州', '揭阳', '台州', '南通', '汕头', '泰安', '阳泉', '济源', '德阳', '梅州', '广元', '廊坊', '连云港', '信阳', '焦作', '随州', '黔东南苗族侗族自治州', '佛山', '淮北', '潜江', '绵阳', '南充', '岳阳', '延安', '衢州', '榆林', '东营', '梧州', '临汾', '沧州', '遵义', '吉安', '孝感', '唐山', '淮南', '忻州', '威海', '萍乡', '宿迁', '珠海', '庆阳', '日照', '铜陵', '滨州', '渭南', '太原', '商丘']




#石家庄 封城时间 2021/1/7——2021/1/29日  比较时间2021/01/01 -2021/05/08(接近春节) 阈值选取为0.04 确定！
# 石家庄一阶城市 13城市
First_order_SJZ = ["石家庄","北京","衡水","秦皇岛","唐山","廊坊","天津","承德","保定","沧州","邯郸","邢台","张家口"]
# 石家庄二阶城市 54城市
Second_order_SJZ =  ['南京', '广州', '长沙', '邯郸', '深圳', '忻州', '长春', '廊坊', '秦皇岛', '锡林郭勒盟', '杭州', '哈尔滨', '三亚', '聊城', '合肥', '沧州', '西安', '衡水', '沈阳', '葫芦岛', '张家口', '苏州', '呼和浩特', '赤峰', '太原', '周口', '天津', '青岛', '潍坊', '菏泽', '济南', '安阳', '北京', '成都', '大同', '滨州', '乌兰察布', '唐山', '临汾', '晋中', '长治', '德州', '浙江', '重庆', '阳泉', '石家庄', '莱芜', '濮阳', '承德', '邢台', '上海', '郑州', '武汉', '保定']
# 石家庄三阶城市 267城市
Third_order_SJZ =  ['绍兴', '齐齐哈尔', '潍坊', '唐山', '哈尔滨', '大同', '三亚', '天门', '盘锦', '儋州', '平顶山', '湖州', '承德', '南昌', '绥化', '佳木斯', '孝感', '长春', '邵阳', '太原', '玉林', '许昌', '莱芜', '青岛', '晋中', '荆门', '丽水', '泰安', '衡水', '合肥', '长治', '梧州', '烟台', '自贡', '湘潭', '鄂尔多斯', '九江', '辽源', '菏泽', '商丘', '惠州', '连云港', '广西壮族自治区', '三门峡', '汕头', '海口', '天津', '临沂', '浙江', '渭南', '德阳', '常州', '铜仁', '雅安', '乌海', '宜宾', '开封', '揭阳', '苏州', '蚌埠', '邯郸', '伊春', '金华', '宜春', '杭州', '银川', '娄底', '毕节', '随州', '忻州', '黄石', '南通', '枣庄', '萍乡', '辽阳', '朝阳', '吉安', '濮阳', '临汾', '南阳', '株洲', '温州', '毕节地区', '衢州', '南京', '铁岭', '广州', '池州', '西安', '贵港', '鹤岗', '商洛', '韶关', '肇庆', '石家庄', '沧州', '阜阳', '中山', '湛江', '包头', '漯河', '乌兰察布', '阜新', '广元', '东营', '遂宁', '南宁', '巴彦淖尔', '抚顺', '恩施土家族苗族自治州', '郑州', '七台河', '大庆', '廊坊', '六安', '达州', '上饶', '赣州', '日照', '周口', '甘孜藏族自治州', '亳州', '驻马店', '盐城', '松原', '延安', '庆阳', '鹤壁', '嘉兴', '马鞍山', '眉山', '泸州', '芜湖', '镇江', '吕梁', '万宁', '清远', '鞍山', '滁州', '焦作', '益阳', '信阳', '云浮', '长沙', '岳阳', '德州', '运城', '沈阳', '锦州', '淄博', '无锡', '白城', '南充', '舟山', '黄冈', '遵义', '通化', '珠海', '广安', '张家口', '成都', '荆州', '绵阳', '本溪', '郴州', '梅州', '北京', '营口', '贺州', '潜江', '衡阳', '双鸭山', '铜仁地区', '怀化', '平凉', '佛山', '淮南', '咸阳', '阳泉', '内蒙古自治区', '鄂州', '安康', '铜陵', '宿州', '晋城', '巴中', '汉中', '福州', '潮州', '黑河', '仙桃', '常德', '济源', '上海', '茂名', '徐州', '滨州', '攀枝花', '洛阳', '厦门', '延边朝鲜族自治州', '昆明', '黄山', '牡丹江', '吉林', '威海', '呼和浩特', '河源', '湘西土家族苗族自治州', '保定', '东莞', '阳江', '台州', '榆林', '乐山', '内江', '贵阳', '宜昌', '东方', '淮北', '保亭黎族苗族自治县', '凉山彝族自治州', '重庆', '朔州', '兰州', '四平', '宿迁', '葫芦岛', '江门', '陵水黎族自治县', '天水', '资阳', '阿坝藏族羌族自治州', '白山', '丹东', '宝鸡', '济南', '淮安', '泉州', '桂林', '武汉', '琼海', '襄阳', '咸宁', '乐东黎族自治县', '铜川', '锡林郭勒盟', '新乡', '济宁', '邢台', '鸡西', '扬州', '张家界', '秦皇岛', '通辽', '安庆', '深圳', '十堰', '大连', '泰州', '安阳', '赤峰', '宁波', '汕尾', '聊城', '永州', '宣城']
# 石家庄四阶城市 339城市
Fourth_order_SJZ =  ['扬州', '温州', '池州', '锡林郭勒盟', '南平', '杭州', '黑河', '酒泉', '舟山', '嘉兴', '武汉', '信阳', '攀枝花', '毕节', '威海', '随州', '澳门', '楚雄彝族自治州', '株洲', '琼中黎族苗族自治县', '许昌', '玉溪', '永州', '白城', '蚌埠', '天水', '晋中', '宣城', '昆明', '漳州', '葫芦岛', '益阳', '鹰潭', '青岛', '东方', '桂林', '中卫', '铜陵', '佳木斯', '抚顺', '安康', '襄阳', '遵义', '海东', '玉林', '湘潭', '黔西南布依族苗族自治州', '抚州', '大同', '岳阳', '盘锦', '咸阳', '鹤壁', '淮南', '亳州', '湘西土家族苗族自治州', '张家口', '吴忠', '南昌', '吕梁', '鞍山', '马鞍山', '柳州', '成都', '兴安盟', '齐齐哈尔', '泰安', '濮阳', '邯郸', '锦州', '天门', '泸州', '内蒙古自治区', '长春', '贵港', '南阳', '白山', '湖州', '保定', '六盘水', '上饶', '临高', '郴州', '三明', '来宾', '滁州', '巴中', '阿坝藏族羌族自治州', '绥化', '乌兰察布', '呼和浩特', '绵阳', '宿州', '大庆', '惠州', '廊坊', '万宁', '红河哈尼族彝族自治州', '秦皇岛', '丽水', '梅州', '西双版纳傣族自治州', '韶关', '荆州', '烟台', '百色', '澄迈', '河池', '莆田', '白沙黎族自治县', '深圳', '大连', '汕尾', '萍乡', '双鸭山', '呼伦贝尔', '漯河', '五指山', '宁波', '驻马店', '黄冈', '内江', '北京', '沈阳', '达州', '合肥', '白银', '三门峡', '宜春', '通化', '芜湖', '伊春', '张掖', '松原', '澄迈县', '泉州', '南宁', '宜宾', '周口', '阳泉', '十堰', '济南', '衡水', '安庆', '东营', '济宁', '通辽', '常德', '南充', '七台河', '常州', '宜昌', '东莞', '宿迁', '毕节地区', '临沂', '琼海', '儋州', '鄂州', '怀化', '福州', '定西', '鄂尔多斯', '商丘', '乐东黎族自治县', '乌海', '太原', '海口', '曲靖', '淮安', '陇南', '焦作', '新疆维吾尔自治区', '广元', '衡阳', '鸡西', '黄石', '邢台', '临高县', '珠海', '乐山', '巴彦淖尔', '赣州', '荆门', '无锡', '揭阳', '阿拉善盟', '汕头', '临沧', '吉安', '屯昌县', '仙桃', '佛山', '丹东', '九江', '金昌', '云浮', '晋城', '石家庄', '洛阳', '银川', '张家界', '定安', '安阳', '临汾', '南通', '保亭黎族苗族自治县', '淄博', '文山壮族苗族自治州', '新余', '营口', '渭南', '平顶山', '临夏回族自治州', '陵水黎族自治县', '中山', '固原', '西安', '连云港', '徐州', '江门', '聊城', '资阳', '德州', '武威', '淮北', '上海', '遂宁', '阳江', '南京', '自贡', '钦州', '贺州', '济源', '辽阳', '海东地区', '浙江', '潮州', '西宁', '景德镇', '菏泽', '龙岩', '运城', '梧州', '朔州', '郑州', '包头', '四平', '恩施土家族苗族自治州', '三亚', '贵阳', '黔南布依族苗族自治州', '哈尔滨', '安顺', '黔东南苗族侗族自治州', '吉林', '崇左', '河源', '日照', '牡丹江', '延边朝鲜族自治州', '辽源', '眉山', '宝鸡', '苏州', '潍坊', '潜江', '朝阳', '石嘴山', '广州', '娄底', '莱芜', '长治', '邵阳', '承德', '昌江黎族自治县', '枣庄', '西藏自治区', '文昌', '大理白族自治州', '铜仁', '茂名', '凉山彝族自治州', '甘南藏族自治州', '铁岭', '德宏傣族景颇族自治州', '昭通', '阜阳', '阜新', '黄山', '湛江', '广安', '盐城', '延安', '保山', '本溪', '普洱', '庆阳', '孝感', '鹤岗', '肇庆', '甘孜藏族自治州', '台州', '泰州', '定安县', '沧州', '赤峰', '绍兴', '开封', '铜仁地区', '金华', '天津', '商洛', '滨州', '汉中', '兰州', '平凉', '防城港', '广西壮族自治区', '厦门', '宁夏回族自治区', '宁德', '铜川', '唐山', '长沙', '六安', '北海', '镇江', '忻州', '重庆', '衢州', '屯昌', '清远', '雅安', '榆林', '咸宁', '新乡', '丽江', '德阳']
#石家庄五阶 336城市
Five_order_SJZ = ['烟台', '文山壮族苗族自治州', '仙桃', '铜川', '泰州', '扬州', '聊城', '鹰潭', '抚顺', '汉中', '无锡', '莱芜', '泰安', '芜湖', '梧州', '钦州', '万宁', '长沙', '平凉', '延安', '常德', '德阳', '常州', '永州', '枣庄', '阿拉善盟', '安康', '沈阳', '文昌', '曲靖', '赣州', '荆州', '甘南藏族自治州', '朝阳', '河源', '保亭黎族苗族自治县', '苏州', '定安', '黄冈', '绥化', '白沙黎族自治县', '青岛', '潮州', '琼海', '衢州', '黔西南布依族苗族自治州', '天津', '马鞍山', '海西蒙古族藏族自治州', '吉安', '亳州', '兴安盟', '朔州', '长治', '南充', '潍坊', '濮阳', '娄底', '玉林', '宿迁', '凉山彝族自治州', '湘潭', '淮安', '包头', '屯昌县', '杭州', '咸宁', '大同', '葫芦岛', '盘锦', '重庆', '雅安', '绵阳', '临高县', '孝感', '渭南', '海东地区', '九江', '益阳', '鹤壁', '张家口', '舟山', '忻州', '龙岩', '白城', '许昌', '佳木斯', '楚雄彝族自治州', '平顶山', '铜陵', '商丘', '大理白族自治州', '西宁', '内江', '新余', '自贡', '海口', '武汉', '资阳', '辽源', '丹东', '三亚', '张家界', '乌海', '海南藏族自治州', '珠海', '攀枝花', '佛山', '莆田', '安顺', '乐山', '六盘水', '廊坊', '儋州', '南平', '临沧', '鹤岗', '承德', '衡阳', '黄山', '随州', '北海', '揭阳', '汕头', '大连', '临汾', '晋中', '阳泉', '黔东南苗族侗族自治州', '衡水', '中山', '桂林', '温州', '琼中黎族苗族自治县', '铜仁', '榆林', '延边朝鲜族自治州', '白银', '商洛', '遵义', '滁州', '潜江', '定西', '淄博', '锦州', '怀化', '丽水', '福州', '哈密地区', '乌兰察布', '中卫', '邵阳', '南昌', '贺州', '三明', '滨州', '大庆', '黄南藏族自治州', '金昌', '济源', '兰州', '甘孜藏族自治州', '六安', '玉溪', '哈尔滨', '通化', '吴忠', '上海', '宿州', '营口', '漯河', '邯郸', '株洲', '唐山', '嘉兴', '辽阳', '天门', '漳州', '阳江', '邢台', '淮南', '宜宾', '屯昌', '鄂尔多斯', '菏泽', '绍兴', '松原', '河池', '日照', '湖州', '北京', '咸阳', '南通', '宜春', '广州', '济南', '哈密', '汕尾', '铁岭', '通辽', '临沂', '长春', '银川', '陇南', '泉州', '运城', '防城港', '鄂州', '惠州', '保定', '石嘴山', '焦作', '洛阳', '迪庆藏族自治州', '广元', '岳阳', '广安', '晋城', '昭通', '铜仁地区', '湛江', '西安', '台州', '固原', '韶关', '巴彦淖尔', '眉山', '红河哈尼族彝族自治州', '达州', '新乡', '赤峰', '恩施土家族苗族自治州', '百色', '昆明', '郑州', '合肥', '阜阳', '盐城', '太原', '白山', '泸州', '十堰', '武威', '石家庄', '崇左', '秦皇岛', '吉林', '嘉峪关', '海东', '荆门', '锡林郭勒盟', '安庆', '湘西土家族苗族自治州', '宁德', '柳州', '庆阳', '丽江', '信阳', '郴州', '临高', '阿坝藏族羌族自治州', '云浮', '贵阳', '德州', '镇江', '周口', '蚌埠', '本溪', '梅州', '昌都', '成都', '深圳', '遂宁', '定安县', '酒泉', '连云港', '徐州', '济宁', '昌都地区', '陵水黎族自治县', '海北藏族自治州', '金华', '南京', '宣城', '池州', '茂名', '双鸭山', '抚州', '四平', '开封', '乐东黎族自治县', '威海', '齐齐哈尔', '东莞', '宜昌', '澳门', '临夏回族自治州', '三门峡', '江门', '黄石', '景德镇', '普洱', '西双版纳傣族自治州', '澄迈县', '襄阳', '毕节地区', '毕节', '南宁', '宝鸡', '东营', '来宾', '淮北', '巴中', '澄迈', '黔南布依族苗族自治州', '东方', '怒江傈僳族自治州', '厦门', '贵港', '清远', '萍乡', '鞍山', '保山', '肇庆', '天水', '呼和浩特', '吕梁', '阜新', '驻马店', '安阳', '昌江黎族自治县', '上饶', '沧州', '张掖', '宁波', '南阳']
#石家庄六阶 城市直接全部包括






#张家界封城时间段 2021/8/1-2021/8/25 封城时间25天，比较时间2021/11/15-2021/5/8
list_ZJJ = ["张家界","常德","长沙","湘西土家族苗族自治州","恩施土家族苗族自治州","益阳","重庆","株洲","岳阳","邵阳","广州","衡阳","深圳"]





# file_path = "F:/封城数据处理/封城数据/石家庄/石家庄四阶/garbage_self_network/deal_01/in/"





#西安日期
# listXData = getdaylist(20211121,20220528)




# 根据路径画图
def drawpicture(filePath,nodes_list_one):
    """
    输入文件路径最后绘制成图G
    """
    global dataMiga
    G = nx.Graph()
    G.add_nodes_from(nodes_list_one)
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



# 计算平均点连通性
def averagenodeconnectivity(file_path,city_name,nodes,listXData):
    """
    返回绘制图表的
    X轴：日期
    Y轴：平均点连通性
    """

    listAverageNodeConnectivity = []
    for i in tqdm (range(len(listXData)),desc="平均点连通性进度",total=len(listXData)):
        # 循环画图
        try:
            filePathInMethon = file_path + listXData[i] +"_"+city_name+".csv"
            G = drawpicture(filePathInMethon,nodes)

        except Exception as problem:
            print("((平均点连通性) error打开迁徙文件出问题：", problem)
        else:
                listAverageNodeConnectivity.append((nx.average_node_connectivity(G)))
    # print("平均点连通性长度： ", (listAverageNodeConnectivity))
    return listAverageNodeConnectivity
    # print("平均点连通性： ", listAverageNodeConnectivity)


# 计算城市度
def get_city_degree(file_path,city_name,nodes,listXData):
    """
    返回绘制图表的
    X轴：日期
    Y轴：平均点连通性
    """
    list_city_degree = []
    for i in range(len(listXData)):
        # 循环画图
        try:
            filePathInMethon = file_path + listXData[i] +"_"+city_name+".csv"
            G = drawpicture(filePathInMethon,nodes)

        except Exception as problem:
            print("((城市度) error打开迁徙文件出问题：", problem)
        else:
            list_city_degree.append(len(G.edges(city_name)))
    return list_city_degree
    # print("城市度： ", list_city_degree)


# 计算边数量
def edge_number(file_path,city_name,nodes,listXData):
    """
    返回绘制图表的
    X轴：日期
    Y轴：平均点连通性
    """
    list_edge_number = []
    for i in range(len(listXData)):
        # 循环画图
        try:
            filePathInMethon = file_path + listXData[i] +"_"+city_name+".csv"
            G = drawpicture(filePathInMethon,nodes)
        except Exception as problem:
            print("((边数量) error打开迁徙文件出问题：", problem)
        else:
            list_edge_number.append(len(G.edges()))
    return list_edge_number
    # print("边数量： ", list_edge_number)


# 计算自然连通性
def naturecconnectivity(file_path,city_name,nodes_list,listXData):
    """
    返回绘制图表的
    X轴：日期
    Y轴：自然连通度数值
    """
    # 时间列表
    listAlgebraicConnectivity = []
    for i in range(len(listXData)):
        # 循环画图
        try:
            filePathInMethon = file_path + listXData[i] +"_"+city_name+".csv"

        except Exception as problem:
            print("(自然连通度) error打开迁徙文件出问题：", problem)
        else:
            G = drawpicture(filePathInMethon,nodes_list)
            # 生成邻接矩阵 直接转为稠密矩阵
            Gadjacency = np.array(nx.adjacency_matrix(G).todense())
            # 求特征值和特征向量
            eigenvalue, featurevector = np.linalg.eig(Gadjacency)
            # 取到所有点
            nodes = len(G.nodes())
            # 定义分子
            molecular = 0
            for eigenvalueNeed in eigenvalue:
                # 开始求自然连通度 ln()里的分子
                molecular = molecular + e ** eigenvalueNeed
            # 自然连通度的值
            algebraicConnectivityValue = log(molecular/nodes, e)
            # 作为Y轴
            listAlgebraicConnectivity.append(algebraicConnectivityValue)
    return listAlgebraicConnectivity
    # print("自然连通度： ", listAlgebraicConnectivity)

def caculate_down_propotion(first_number,second_number):
    """
    计算时间顺序的下降比例
    :param first_number:  必须是列表参数的形式
    :param second_number: 必须是列表参数的形式
    :return:
    """
    # 衡量下降
    #最终储存的比例列表

    # 第一个
    num_old = 0
    for s in first_number:
        num_old = num_old + s
    # print(num_old)

    # 第二个
    num_new = 0
    for t in second_number:
        num_new = num_new + t
    # print(num_new)


    # result = (num_old - num_new) / num_new
    result = (num_old - num_new) / num_old

    return round(result, 4)


def down_propotion_slice(list_name,flags):
    list_propotion_one = []
    list_propotion_two = []
    list_propotion_three = []
    list_propotion_four = []
    list_name_list = [list_propotion_one,list_propotion_two,list_propotion_three]
    for index_name,listname in zip(list_name,list_name_list):
        #石家庄
        #range(0,115), range(22, 137)
        #西安
        #range(0,131), range(22, 153)
        if flags == 1:
            for i, j in zip(range(0,115), range(22, 137)):
                first_list = index_name[i:j]
                second_list = index_name[i + 22:j + 22]
                listname.append(caculate_down_propotion(first_list, second_list))
        elif flags == 0:
            for i, j in zip(range(0,131), range(22, 153)):
                first_list = index_name[i:j]
                second_list = index_name[i + 22:j + 22]
                listname.append(caculate_down_propotion(first_list, second_list))
        elif flags == 2:
            for i, j in zip(range(0, 72), range(25, 97)):
                first_list = index_name[i:j]
                second_list = index_name[i + 25:j + 25]
                listname.append(caculate_down_propotion(first_list, second_list))
        elif flags == 3:
            for i, j in zip(range(0, 64), range(27, 91)):
                first_list = index_name[i:j]
                second_list = index_name[i + 27:j + 27]
                listname.append(caculate_down_propotion(first_list, second_list))
    # print((list_propotion))
    # print(len(list_propotion_one))
    print((list_propotion_one))
    print((list_propotion_two))
    print((list_propotion_three))
    # print((list_propotion_four))
    print(len(list_propotion_three))
    return list_propotion_one,list_propotion_two,list_propotion_three
    # print((list_propotion))



def merge_data(one,two):
    """

    :param list_one: 原始列表
    :param list_two: 需要加入到第一个列表的列表
    :return:
    """
    # for one ,two in zip(list_one,list_two):
    # copy_two = two[:]
    # for i in copy_two:
    #     two.append(i)
    for i ,j in zip(range(len(two)),two):
        # if j <= 0:
        #     one[i] = one[i] + (2*two[i])
        # else:
            one[i] = one[i] - (two[i])
    print (one)
    # print(len(one))
    return one

def merge_data_new(one,two):
    """

    :param list_one: 原始列表
    :param list_two: 需要加入到第一个列表的列表
    :return:
    """
    # for one ,two in zip(list_one,list_two):
    # copy_two = two[:]
    # for i in copy_two:
    #     two.append(i)
    for i,j in zip(two[75:95],range(75,95)):
        if i<=0:
            one[j] = one[j]+two[j]
        else:
            one[j] = one[j] - two[j]
    print(one)
    print(len(one))
    return one




def function_encapsulation(first_data,third_data,fourth_data,listXData_SJz,
                           five_data,seven_data,eight_data,listXData_xian):
    print(first_data)
    print(third_data)
    print(fourth_data)
    print(five_data)
    print(seven_data)
    print(eight_data)

    def format_fn(tick_val, tick_pos):
        if int(tick_val) in range(len(listXData_SJz)):
            return str(listXData_SJz[int(tick_val)])
        else:
            return ''

    fig = plt.figure(figsize=(6,4))  # ,dpi=450  10, 4 (6,8)
    ax1 = fig.add_subplot(111)
    ax1.xaxis.set_major_formatter(FuncFormatter(format_fn))
    ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
    # plt.ylim((-5, 40))
    # 横坐标每个值旋转90度
    plt.xticks(rotation=45)

    # 坐标轴ticks的字体大小
    ax1.set_xlabel('日期', fontsize=12)  # 为x轴添加标签
    ax1.set_ylabel('经济变化比例', fontsize=12)  # 为y轴添加标签  数值
    ax1.legend()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams["axes.unicode_minus"] = False

    # 根据需要设置最大最小值，这里设置最大值为1.最小值为0
    # 数据归一化
    tool = MinMaxScaler(feature_range=(0, 1))
    # first_data = tool.fit_transform(array(first_data).reshape(-1,1)).tolist()
    # third_data = tool.fit_transform(array(third_data).reshape(-1,1)).tolist()
    # fourth_data = tool.fit_transform(array(fourth_data).reshape(-1,1)).tolist()

    # 石家庄对比经济变化比例   2021年石家庄封城经济变化比例(含节假日)
    # plt.title("2021年石家庄市经济变化比例",fontsize=12)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)


    plt.plot(listXData_SJz, first_data,  linewidth=2,  label="平均点连通性") #"4-",
    # plt.plot(listXData_SJz, second_data, linewidth=2, label='城市度')  # , "1--"
    plt.plot(listXData_SJz, third_data, linewidth=2, label='边数量')  # , ".-"
    plt.plot(listXData_SJz, fourth_data, linewidth=2, label='平均最短路径长度')  # , ".-"

    ax1.legend(fontsize=12)  # fontsize=12

    plt.axhline(y=0, xmin=0, xmax=1,c="r", ls="--", lw=2)

    # plt.axhspan(ymin=0.4, ymax=0.6, facecolor="g", alpha=0.2)

    plt.axhspan(ymin=-0.4, ymax=-0.6, facecolor="g", alpha=0.2)
    # xmin=33, xmax=62
    plt.axvspan(xmin=33, xmax=59, facecolor='r', alpha=0.2)

    # plt.scatter(6, 1, s=50, color='cyan')
    # plt.plot([6, 6], [1, 0], 'x--', lw=1.5)
    # plt.text(0, 0.90, r'封城开始', fontdict={'size': '12', 'color': 'black'})
    #
    # plt.scatter(28, 1, s=50, color='cyan')
    # plt.plot([28, 28], [1, 0], 'x--', lw=1.5)
    # plt.text(27, 0.90, r'封城结束', fontdict={'size': '12', 'color': 'black'})




    # def format_fn_xian(tick_val, tick_pos):
    #     if int(tick_val) in range(len(listXData_xian)):
    #         return str(listXData_xian[int(tick_val)])#[4:8]
    #     else:
    #         return ''
    #
    # ax2 = fig.add_subplot(111)
    # ax2.xaxis.set_major_formatter(FuncFormatter(format_fn_xian))
    # ax2.xaxis.set_major_locator(MaxNLocator(integer=True))
    #
    # # 坐标轴ticks的字体大小
    # ax2.set_xlabel('日期', fontsize=12)  # 为x轴添加标签
    # ax2.set_ylabel('经济变化比例', fontsize=12)  # 为y轴添加标签  数值
    #
    # ax2.legend()
    #
    # plt.plot(listXData_xian, five_data, color="#4F9DA6", linewidth=2, label='平均点连通性')  # "4-",
    # # plt.plot(listXData_xian, six_data, color="#1663a9", linewidth=2, label='城市度')  # , "1--"
    # plt.plot(listXData_xian, seven_data, color="#FFAD5A", linewidth=2, label='边数量')  # , ".-"
    # plt.plot(listXData_xian, eight_data, color="#FF5959", linewidth=2, label='平均最短路径长度')  # , ".-"
    #
    # plt.title("2022年齐齐哈尔市经济变化比例", fontsize=12)
    # plt.xticks(fontsize=12, rotation=45)
    # plt.yticks(fontsize=12)
    # plt.legend(fontsize=12,)  #
    #
    # plt.axhline(y=0, xmin=0, xmax=1, c="r", ls="--", lw=2)
    #
    # plt.axhspan(ymin=-0.4, ymax=-0.6, facecolor="g", alpha=0.2)
    #
    # # plt.axvspan(xmin=54, xmax=54, facecolor='r', alpha=0.2)
    # plt.axvspan(xmin=39, xmax=57, facecolor='r', alpha=0.2)
    #
    # # plt.scatter(22, 1, s=50, color='cyan')
    # # plt.plot([22, 22], [1, 0], 'x--', lw=1.5)
    # # plt.text(22, 0.90, r'封城开始', fontdict={'size': '12', 'color': 'black'})
    # #
    # # plt.scatter(45, 1, s=50, color='cyan')
    # # plt.plot([45, 45], [1, 0], 'x--', lw=1.5)
    # # plt.text(45, 0.90, r'封城结束', fontdict={'size': '12', 'color': 'black'})
    #


    fig.tight_layout()
    png1 = io.BytesIO()
    plt.savefig(png1, format="png", dpi=500, pad_inches=.1, bbox_inches='tight')
    # Load this image into PIL
    png2 = Image.open(png1)

    # Save as TIFF
    png2.save("LOCK_SJZ_NoTitle.tiff")
    png1.close()
    plt.show()





def function_encapsulation_sigle(first_data,second_data,third_data,listXData_SJz):
    print(first_data)
    print(second_data)
    print(third_data)


    def format_fn(tick_val, tick_pos):
        if int(tick_val) in range(len(listXData_SJz)):
            return str(listXData_SJz[int(tick_val)])
        else:
            return ''

    fig = plt.figure(figsize=(10,4))  # ,dpi=450  10, 4 (6,8)
    ax1 = fig.add_subplot(121)
    ax1.xaxis.set_major_formatter(FuncFormatter(format_fn))
    ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
    # plt.ylim((-5, 40))
    # 横坐标每个值旋转90度
    plt.xticks(rotation=45)

    # 坐标轴ticks的字体大小
    ax1.set_xlabel('日期', fontsize=12)  # 为x轴添加标签
    ax1.set_ylabel('经济变化比例', fontsize=12)  # 为y轴添加标签  数值
    ax1.legend()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams["axes.unicode_minus"] = False

    # 根据需要设置最大最小值，这里设置最大值为1.最小值为0
    # 数据归一化
    tool = MinMaxScaler(feature_range=(0, 1))
    # first_data = tool.fit_transform(array(first_data).reshape(-1,1)).tolist()

    # 石家庄对比经济变化比例
    plt.title("2021年张家界封城经济变化比例(含节假日)",fontsize=12)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)


    plt.plot(listXData_SJz, first_data,  linewidth=2,  label="平均点连通性") #"4-",
    # plt.plot(listXData_SJz, second_data, linewidth=2, label='城市度')  # , "1--"
    plt.plot(listXData_SJz, second_data, linewidth=2, label='边数量')  # , ".-"
    plt.plot(listXData_SJz, third_data, linewidth=2, label='平均最短路径长度')  # , ".-"

    ax1.legend(fontsize=12)  # fontsize=12

    plt.axhline(y=0, xmin=0, xmax=1,c="r", ls="--", lw=2)

    # plt.axhspan(ymin=0.4, ymax=0.6, facecolor="g", alpha=0.2)

    plt.axhspan(ymin=-0.4, ymax=-0.6, facecolor="g", alpha=0.2)
    # xmin=33, xmax=62
    plt.axvspan(xmin=36, xmax=62, facecolor='r', alpha=0.2)
    # plt.scatter(6, 1, s=50, color='cyan')
    # plt.plot([6, 6], [1, 0], 'x--', lw=1.5)
    # plt.text(0, 0.90, r'封城开始', fontdict={'size': '12', 'color': 'black'})
    #
    # plt.scatter(28, 1, s=50, color='cyan')
    # plt.plot([28, 28], [1, 0], 'x--', lw=1.5)
    # plt.text(27, 0.90, r'封城结束', fontdict={'size': '12', 'color': 'black'})






    fig.tight_layout()
    plt.show()





def draw_onePic_plot(first_data,second_data,third_data,fourth_data,listXData,title_name):

    def format_fn(tick_val, tick_pos):
        if int(tick_val) in range(len(listXData)):
            return str(listXData[int(tick_val)])
        else:
            return ''

    fig = plt.figure(figsize=(10, 12))  # ,dpi=450
    ax1 = fig.add_subplot(111)
    ax1.xaxis.set_major_formatter(FuncFormatter(format_fn))
    ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
    # plt.ylim((-5, 40))
    # 横坐标每个值旋转90度
    plt.xticks(rotation=45)

    # 坐标轴ticks的字体大小
    ax1.set_xlabel('日期', fontsize=12)  # 为x轴添加标签
    ax1.set_ylabel('数值', fontsize=12)  # 为y轴添加标签  数值
    ax1.legend()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # 根据需要设置最大最小值，这里设置最大值为1.最小值为0
    # 数据归一化
    tool = MinMaxScaler(feature_range=(0, 1))
    first_data = tool.fit_transform(array(first_data).reshape(-1,1)).tolist()
    second_data = tool.fit_transform(array(second_data).reshape(-1,1)).tolist()
    third_data = tool.fit_transform(array(third_data).reshape(-1,1)).tolist()
    fourth_data = tool.fit_transform(array(fourth_data).reshape(-1,1)).tolist()

    plt.title(title_name,fontsize=12)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)


    plt.plot(listXData, first_data,  linewidth=2,  label='一阶') #"4-",
    plt.plot(listXData, second_data, linewidth=2,  label='二阶')#, "1--"
    plt.plot(listXData, third_data, linewidth=2,  label='三阶')#, ".-"
    plt.plot(listXData, fourth_data, linewidth=2,  label='四阶') #, ".-"

    # plt.plot(listXData, first_data, linewidth=2, color="#1663a9", label='平均点连通性')  # "4-",
    # plt.plot(listXData, second_data, linewidth=2, color="#FFAD5A", label='城市度')  # , "1--"
    # plt.plot(listXData, third_data, linewidth=2, color="#FF5959", label='边数量')  # , ".-"
    # plt.plot(listXData, fourth_data, linewidth=2, color="#4F9DA6", label='平均最短路径长度')  #


    plt.scatter(6, 1, s=50, color='cyan')
    plt.plot([6, 6], [1, 0], 'x--', lw=1.5)
    plt.text(0, 0.90, r'封城开始', fontdict={'size': '12', 'color': 'black'})

    plt.scatter(28, 1, s=50, color='cyan')
    plt.plot([28, 28], [1, 0], 'x--', lw=1.5)
    plt.text(27, 0.90, r'封城结束', fontdict={'size': '12', 'color': 'black'})
    plt.legend(fontsize=12,loc="lower right")#fontsize=12

    # plt.scatter(92, 1, s=50, color='cyan')
    # plt.plot([92, 92], [1, 0], 'x--', lw=1.5)
    # plt.text(91, 0.9, r'清明节', fontdict={'size': '12', 'color': 'black'})
    #
    # plt.scatter(120, 1, s=50, color='cyan')
    # plt.plot([120, 120], [1, 0], 'x--', lw=1.5)
    # plt.text(119, 0.9, r'劳动节', fontdict={'size': '12', 'color': 'black'})
    fig.tight_layout()
    plt.show()

















city_list_qqhe=["齐齐哈尔",'哈尔滨', '大庆', '呼伦贝尔', '兴安盟', '黑河', '绥化', '天津', '白城', '北京', '长春', '廊坊', '青岛', '大连']

if __name__ == '__main__':

    file_path_SJZ = "F:/封城数据处理/封城数据/石家庄/石家庄一阶/deal_03/"
    file_path_xian = "F:/封城数据处理/封城数据/西安/西安一阶/deal_03/"
    file_path_zjj = "F:/封城数据处理/封城数据/张家界/张家界一阶/deal_03/"
    file_path_qqhe = "F:/封城数据处理/封城数据/齐齐哈尔/齐齐哈尔一阶/deal_03/"


    # # 石家庄有封城日期
    listXData_Lock_sjz = getdaylist(20201201, 20210508)
    print(len(listXData_Lock_sjz))
    # 石家庄对比日期 农历   比较有可比性的时间 20221030,20230406   20221113, 20230420   20220201, 20220709
    listXData_contrast_sjz = getdaylist(20211201, 20220508)
    print(len(listXData_contrast_sjz))



    # 西安有封城日期
    listXData_Lock_xian = getdaylist(20211115, 20220508)
    # print(len(listXData_Lock_xian))
    # # 西安对比日期 农历   20210105, 20210628
    # listXData_contrast = getdaylist(20210105, 20210628)
    listXData_contrast = getdaylist(20201115, 20210508)
    print(len(listXData_contrast))




    # # 张家界现有封城日期 20210801,20210825
    # listXData_Lock_zjj = getdaylist(20210601,20210930)
    # print(len(listXData_Lock_zjj))
    # # 石家庄对比日期 农历   比较有可比性的时间 20221030,20230406   20221113, 20230420   20220201, 20220709  72
    # listXData_contrast_zjj = getdaylist(20210626,20210905)
    # print(len(listXData_contrast_zjj))


    #齐齐哈尔  20201201, 20210301  91天 27天封城
    listXData_Lock_qqhe = getdaylist(20201101, 20210401)  #(20201101, 20210401)
    print(len(listXData_Lock_qqhe))
    # 石家庄对比日期 农历   比较有可比性的时间 20221030,20230406   20221113, 20230420   20220201, 20220709  72
    listXData_contrast_qqhe = getdaylist(20201204, 20210205)
    print(len(listXData_contrast_qqhe))




    # 石家庄对比日期 公历
    # print(getdaylist(20211201, 20220508))

    #石家庄处理后的日期（第一幅）
    list_SJZ_xticks =['20201201', '20201202', '20201203', '20201204', '20201205', '20201206', '20201207', '20201208', '20201209', '20201210', '20201211', '20201212', '20201213', '20201214', '20201215', '20201216', '20201217', '20201218', '20201219', '20201220', '20201221', '20201222', '20201223', '20201224', '20201225', '20201226', '20201227', '20201228', '20201229', '20201230', '20201231', '20210101', '20210102', '20210103', '20210104', '20210105', '20210106', '20210107', '20210108', '20210109', '20210110', '20210111', '20210112', '20210113', '20210114', '20210115', '20210116', '20210117', '20210118', '20210119', '20210120', '20210121', '20210122', '20210123', '20210124', '20210125', '20210126', '20210127', '20210128', '20210129', '20210130', '20210131', '20210201', '20210202', '20210203', '20210204', '20210205', '20210206', '20210207', '20210208', '20210209', '20210210', '20210211', '20210212', '20210213', '20210214', '20210215', '20210216', '20210217', '20210218', '20210219', '20210220', '20210221', '20210222', '20210223', '20210224', '20210225', '20210226', '20210227', '20210228', '20210301', '20210302', '20210303', '20210304', '20210305', '20210306', '20210307', '20210308', '20210309', '20210310', '20210311', '20210312', '20210313', '20210314', '20210315', '20210316', '20210317', '20210318', '20210319', '20210320', '20210321', '20210322', '20210323', '20210324', '20210325']
    # list_SJZ_xticks=getdaylist(20211201, 20220325)

    # print("石家庄日期长度",len(list_SJZ_xticks))
    # list_xian_xticks = ['20211115', '20211116', '20211117', '20211118', '20211119', '20211120', '20211121', '20211122', '20211123', '20211124', '20211125', '20211126', '20211127', '20211128', '20211129', '20211130', '20211201', '20211202', '20211203', '20211204', '20211205', '20211206', '20211207', '20211208', '20211209', '20211210', '20211211', '20211212', '20211213', '20211214', '20211215', '20211216', '20211217', '20211218', '20211219', '20211220', '20211221', '20211222', '20211223', '20211224', '20211225', '20211226', '20211227', '20211228', '20211229', '20211230', '20211231', '20220101', '20220102', '20220103', '20220104', '20220105', '20220106', '20220107', '20220108', '20220109', '20220110', '20220111', '20220112', '20220113', '20220114', '20220115', '20220116', '20220117', '20220118', '20220119', '20220120', '20220121', '20220122', '20220123', '20220124', '20220125', '20220126', '20220127', '20220128', '20220129', '20220130', '20220131', '20220201', '20220202', '20220203', '20220204', '20220205', '20220206', '20220207', '20220208', '20220209', '20220210', '20220211', '20220212', '20220213', '20220214', '20220215', '20220216', '20220217', '20220218', '20220219', '20220220', '20220221', '20220222', '20220223', '20220224', '20220225', '20220226', '20220227', '20220228', '20220301', '20220302', '20220303', '20220304', '20220305', '20220306', '20220307', '20220308', '20220309', '20220310', '20220311', '20220312', '20220313', '20220314', '20220315', '20220316', '20220317', '20220318', '20220319', '20220320', '20220321', '20220322', '20220323', '20220324', '20220325']

    # 西安处理后的日期（第一幅）
    list_xian_xticks = ['20211123', '20211124', '20211125', '20211126', '20211127', '20211128', '20211129', '20211130', '20211201', '20211202', '20211203', '20211204', '20211205', '20211206', '20211207', '20211208', '20211209', '20211210', '20211211', '20211212', '20211213', '20211214', '20211215', '20211216', '20211217', '20211218', '20211219', '20211220', '20211221', '20211222', '20211223', '20211224', '20211225', '20211226', '20211227', '20211228', '20211229', '20211230', '20211231', '20220101', '20220102', '20220103', '20220104', '20220105', '20220106', '20220107', '20220108', '20220109', '20220110', '20220111', '20220112', '20220113', '20220114', '20220115', '20220116', '20220117', '20220118', '20220119', '20220120', '20220121', '20220122', '20220123', '20220124', '20220125', '20220126', '20220127', '20220128', '20220129', '20220130', '20220131', '20220201', '20220202', '20220203', '20220204', '20220205', '20220206', '20220207', '20220208', '20220209', '20220210', '20220211', '20220212', '20220213', '20220214', '20220215', '20220216', '20220217', '20220218', '20220219', '20220220', '20220221', '20220222', '20220223', '20220224', '20220225', '20220226', '20220227', '20220228', '20220301', '20220302', '20220303', '20220304', '20220305', '20220306', '20220307', '20220308', '20220309', '20220310', '20220311', '20220312', '20220313', '20220314', '20220315', '20220316', '20220317', '20220318', '20220319', '20220320', '20220321', '20220322', '20220323', '20220324', '20220325', '20220326', '20220327', '20220328', '20220329', '20220330', '20220331', '20220401', '20220402']
    # list_xian_xticks = getdaylist(20201123, 20210402)
    # print("西安日期长度",len(list_xian_xticks))





    # file_path = "F:/封城数据处理/封城数据/齐齐哈尔/齐齐哈尔一阶/deal_03/"
    #
    # list_qqhe = ["哈尔滨", "呼伦贝尔", "齐齐哈尔", "兴安盟", "大庆", "黑河", "天津", "北京", "绥化", "白城", "廊坊",
    #              "沈阳", "大连"]
    #
    # print(averagenodeconnectivity(file_path, "齐齐哈尔", list_qqhe,getdaylist(20201101, 20210401)))
    # print(get_city_degree(file_path, "齐齐哈尔", list_qqhe,getdaylist(20201101, 20210401)))
    # print(edge_number(file_path, "齐齐哈尔", list_qqhe,getdaylist(20201101, 20210401)))
    # print(naturecconnectivity(file_path, "齐齐哈尔", list_qqhe,getdaylist(20201101, 20210401)))



    # list_index_name_Lock_zjj = [averagenodeconnectivity(file_path_zjj, "张家界", list_ZJJ,listXData_Lock_zjj),
    #                         get_city_degree(file_path_zjj, "张家界", list_ZJJ,listXData_Lock_zjj),
    #                         edge_number(file_path_zjj, "张家界", list_ZJJ,listXData_Lock_zjj),
    #                         naturecconnectivity(file_path_zjj, "张家界", list_ZJJ,listXData_Lock_zjj)]
    #
    #
    # list_propotion_one_Lock_zjj, list_propotion_two_Lock_zjj, list_propotion_three_Lock_zjj, list_propotion_four_Lock_zjj \
    #     = down_propotion_slice(list_index_name_Lock_zjj,2)
    #
    # function_encapsulation_sigle( [-l for l in list_propotion_one_Lock_zjj],[-l for l in list_propotion_two_Lock_zjj],
    #                               [-l for l in list_propotion_three_Lock_zjj],
    #                               [-l for l in list_propotion_four_Lock_zjj],
    #                         # list_propotion_one_Lock_zjj, list_propotion_two_Lock_zjj, list_propotion_three_Lock_zjj,
    #                         #       list_propotion_four_Lock_zjj,
    #                               listXData_contrast_zjj)








    list_index_name_Lock_qqhe = [averagenodeconnectivity(file_path_qqhe, "齐齐哈尔", city_list_qqhe, listXData_Lock_qqhe),
                                # get_city_degree(file_path_qqhe, "齐齐哈尔", city_list_qqhe, listXData_Lock_qqhe),
                                edge_number(file_path_qqhe, "齐齐哈尔", city_list_qqhe, listXData_Lock_qqhe),
                                naturecconnectivity(file_path_qqhe, "齐齐哈尔", city_list_qqhe, listXData_Lock_qqhe)]

    list_propotion_one_Lock_qqhe, list_propotion_two_Lock_qqhe, list_propotion_three_Lock_qqhe \
        = down_propotion_slice(list_index_name_Lock_qqhe, 3)
    # #
    # function_encapsulation_sigle(
    #                             # [-l for l in list_propotion_one_Lock_zjj],
    #                             # [-l for l in list_propotion_two_Lock_zjj],
    #                             #  [-l for l in list_propotion_three_Lock_zjj],
    #                             #  [-l for l in list_propotion_four_Lock_zjj],
    #                              list_propotion_one_Lock_qqhe, list_propotion_two_Lock_qqhe,
    #                              list_propotion_three_Lock_qqhe,
    #                              listXData_contrast_qqhe)




    #齐齐哈尔  0.01是最合适的阈值
    # list_index_name_contrast_qqhe = [
    #     averagenodeconnectivity(file_path_qqhe, "齐齐哈尔", city_list_qqhe, listXData_Lock_qqhe),
    #     # get_city_degree(file_path_qqhe, "齐齐哈尔", city_list_qqhe, listXData_Lock_qqhe),
    #     edge_number(file_path_qqhe, "齐齐哈尔", city_list_qqhe, listXData_Lock_qqhe),
    #     naturecconnectivity(file_path_qqhe, "齐齐哈尔", city_list_qqhe, listXData_Lock_qqhe)]
    #
    # list_propotion_one_contrast_qqhe, list_propotion_two_contrast_qqhe, list_propotion_contrast_qqhe \
    #     = down_propotion_slice(list_index_name_contrast_qqhe, 3)
    # #
    # function_encapsulation_sigle(
    #     # [-l for l in list_propotion_one_Lock_zjj],
    #     # [-l for l in list_propotion_two_Lock_zjj],
    #     #  [-l for l in list_propotion_three_Lock_zjj],
    #     #  [-l for l in list_propotion_four_Lock_zjj],
    #     list_propotion_one_contrast_qqhe, list_propotion_two_contrast_qqhe,
    #     list_propotion_contrast_qqhe,
    #     listXData_contrast_qqhe)







    # draw_onePic_plot(averagenodeconnectivity(file_path_qqhe, "齐齐哈尔", city_list_qqhe, listXData_Lock_qqhe),
    #                             get_city_degree(file_path_qqhe, "齐齐哈尔", city_list_qqhe, listXData_Lock_qqhe),
    #                             edge_number(file_path_qqhe, "齐齐哈尔", city_list_qqhe, listXData_Lock_qqhe),
    #                             naturecconnectivity(file_path_qqhe, "齐齐哈尔", city_list_qqhe, listXData_Lock_qqhe),
    #                         listXData_Lock_qqhe,"齐齐哈尔市")









    #
    # list_index_name_Lock_xian = [averagenodeconnectivity(file_path_xian, "西安", First_order_xian,listXData_Lock_xian),
    #                         # get_city_degree(file_path_xian, "西安", First_order_xian,listXData_Lock_xian),
    #                         edge_number(file_path_xian, "西安", First_order_xian,listXData_Lock_xian),
    #                         naturecconnectivity(file_path_xian, "西安", First_order_xian,listXData_Lock_xian)]
    #
    #
    # list_propotion_one_Lock_xian, list_propotion_two_Lock_xian, list_propotion_three_Lock_xian\
    #     = down_propotion_slice(list_index_name_Lock_xian,0)







    # list_index_name_contrast_xian = [averagenodeconnectivity(file_path_xian, "西安", First_order_xian, listXData_contrast),
    #                             get_city_degree(file_path_xian, "西安", First_order_xian, listXData_contrast),
    #                             edge_number(file_path_xian, "西安", First_order_xian, listXData_contrast),
    #                             naturecconnectivity(file_path_xian, "西安", First_order_xian, listXData_contrast)]
    #
    # list_propotion_one_contrast_xian, list_propotion_two_contrast_xian, list_propotion_three_contrast_xian, list_propotion_four_contrast_xian \
    #     = down_propotion_slice(list_index_name_contrast_xian,0)
    #



    # 没有做过处理的对比图
    # function_encapsulation(list_propotion_one_Lock, list_propotion_two_Lock, list_propotion_three_Lock,
    #                        list_propotion_four_Lock,
    #                        list_xian_xticks,
    #                        list_propotion_one_contrast,
    #                        list_propotion_two_contrast,
    #                        list_propotion_three_contrast,
    #                        list_propotion_four_contrast,
    #                        list_xian_xticks)



    # 使用公历/农历时间减去正常时间段后绘制的对比图
    # function_encapsulation(merge_data(list_propotion_one_Lock_xian, list_propotion_one_contrast[60:75]),
    #                        merge_data(list_propotion_two_Lock_xian, list_propotion_two_contrast[60:75]),
    #                        merge_data(list_propotion_three_Lock_xian, list_propotion_three_contrast[60:75]),
    #                        merge_data(list_propotion_four_Lock_xian, list_propotion_four_contrast[60:75]),
    #                        list_xian_xticks,
    #                        list_propotion_one_contrast,
    #                        list_propotion_two_contrast,
    #                        list_propotion_three_contrast,
    #                        list_propotion_four_contrast,
    #                        list_xian_xticks)



    #
    #
    # #
    list_index_name_Lock_sjz=[averagenodeconnectivity(file_path_SJZ,"石家庄",First_order_SJZ,listXData_Lock_sjz),
                     # get_city_degree(file_path_SJZ,"石家庄",First_order_SJZ,listXData_Lock_sjz),
                     edge_number(file_path_SJZ,"石家庄",First_order_SJZ,listXData_Lock_sjz),
                     naturecconnectivity(file_path_SJZ,"石家庄",First_order_SJZ,listXData_Lock_sjz)]

    list_propotion_one_Lock_sjz,list_propotion_two_Lock_sjz,list_propotion_three_Lock_sjz  \
        = down_propotion_slice(list_index_name_Lock_sjz,1)

    # list_index_name_contrast_sjz = [averagenodeconnectivity(file_path_SJZ, "石家庄", First_order_SJZ, listXData_contrast_sjz),
    #                    get_city_degree(file_path_SJZ, "石家庄", First_order_SJZ, listXData_contrast_sjz),
    #                    edge_number(file_path_SJZ, "石家庄", First_order_SJZ, listXData_contrast_sjz),
    #                    naturecconnectivity(file_path_SJZ, "石家庄", First_order_SJZ, listXData_contrast_sjz)]
    #
    # list_propotion_one_contrast_sjz, list_propotion_two_contrast_sjz, list_propotion_three_contrast_sjz, list_propotion_four_contrast_sjz \
    # = down_propotion_slice(list_index_name_contrast_sjz,1)
    # #
    # listy_one = [list_propotion_one_contrast_sjz, list_propotion_two_contrast_sjz, list_propotion_three_contrast_sjz, list_propotion_four_contrast_sjz]
    #
    # five =  [-0.010100000000000001, 0.0773, 0.1064, 0.1247, 0.1491, 0.16310000000000002, 0.175, 0.18860000000000002, 0.19960000000000003, 0.21559999999999999, 0.19879999999999998, 0.172, 0.1432, 0.13329999999999997, 0.11680000000000001, 0.08779999999999999, 0.07419999999999993, 0.03920000000000001, -0.00550000000000006, -0.051899999999999946, -0.09209999999999996, -0.1301, -0.14919999999999994, -0.18059999999999998, -0.20080000000000003, -0.24380000000000002, -0.2980999999999999, -0.36050000000000004, -0.4409, -0.52, -0.6102000000000001, -0.7545999999999999, -0.911, -1.1006, -1.3441, -1.5327000000000002, -1.6772, -1.7381, -1.8168000000000002, -1.7979, -1.7492, -1.6605999999999999, -1.583, -1.546, -1.5038, -1.4127, -1.3762, -1.2713, -1.2007, -1.1093, -1.0165, -0.9414, -0.8583000000000001, -0.7516, -0.6425000000000001, -0.5207, -0.4208, -0.3708, -0.3404, -0.3639, -0.3786, -0.3875, -0.3443, -0.3035, -0.2666, -0.2131, -0.17109999999999997, -0.1717, -0.1732, -0.1749, -0.0446, -0.0329, -0.0136, 0.0184, 0.0367, 0.0696, 0.1072, 0.1322, 0.1583, 0.201, 0.236, 0.2728, 0.3117, 0.3443, 0.3567, 0.374, 0.3961, 0.4043, 0.4058, 0.4259, 0.434, 0.4442, 0.4536, 0.4643, 0.4685, 0.4618, 0.4462, 0.4366, 0.4156, 0.3964, 0.3782, 0.341, 0.3046, 0.2677, 0.2198, 0.1765, 0.1346, 0.1079, 0.0795, 0.0664, 0.0757, 0.0508, 0.0352, 0.0191, -0.0011, -0.02, -0.0431, -0.0565, -0.0365, -0.0567, -0.0631, -0.0656, -0.0754, -0.0853, -0.0819, -0.0818, -0.0726, -0.0974, -0.0929, -0.1192, -0.151]
    #
    # print(len(five))
    #
    # six =  [0.10400000000000001, 0.159, 0.1913, 0.2318, 0.2671, 0.3168, 0.363, 0.3715, 0.3665, 0.3593, 0.34230000000000005, 0.32170000000000004, 0.33559999999999995, 0.3692, 0.3853, 0.3793, 0.3548, 0.296, 0.25639999999999996, 0.23879999999999996, 0.2021, 0.15140000000000003, 0.1325, 0.09309999999999996, 0.04660000000000003, 0.008199999999999985, -0.06940000000000002, -0.1565, -0.2464, -0.3539, -0.4739, -0.621, -0.795, -1.0078, -1.288, -1.5969000000000002, -1.863, -2.1718, -2.3948, -2.424, -2.3831, -2.27, -2.064, -1.8434, -1.6872, -1.5489, -1.4425, -1.322, -1.1582999999999999, -1.0035, -0.8779, -0.7657999999999999, -0.6759000000000001, -0.5791999999999999, -0.4961, -0.41209999999999997, -0.3341, -0.27599999999999997, -0.24309999999999998, -0.1995, -0.1661, -0.1386, -0.1084, -0.08750000000000001, -0.0819, -0.084, -0.0822, -0.0683, -0.05059999999999999, -0.039400000000000004, -0.0154, -0.0154, -0.0154, -0.0154, -0.0092, -0.0031, 0.0031, 0.0092, 0.0215, 0.0399, 0.0579, 0.0729, 0.0848, 0.0939, 0.1, 0.1061, 0.1121, 0.1152, 0.1182, 0.1212, 0.1212, 0.1242, 0.1242, 0.1273, 0.1273, 0.1273, 0.1159, 0.1074, 0.0957, 0.0839, 0.0629, 0.0319, 0.0097, -0.0131, -0.0298, -0.0468, -0.0572, -0.0678, -0.0785, -0.0822, -0.0825, -0.0828, -0.0724, -0.0761, -0.0727, -0.0764, -0.0729, -0.0694, -0.0586, -0.055, -0.0444, -0.0339, -0.0235, -0.0033, 0.0065, 0.0194, 0.0289, 0.0383, 0.0414, 0.0476, 0.0538]
    #
    # seven = [0.0878, 0.1037, 0.1195, 0.1325, 0.1486, 0.15740000000000004, 0.1658, 0.18039999999999998, 0.19209999999999997, 0.20819999999999997, 0.20229999999999998, 0.19030000000000002, 0.19310000000000005, 0.19240000000000002, 0.18840000000000007, 0.16619999999999996, 0.15419999999999995, 0.12060000000000004, 0.07919999999999999, 0.046999999999999986, 0.017199999999999993, -0.018799999999999983, -0.04510000000000003, -0.07640000000000002, -0.10930000000000001, -0.15280000000000002, -0.20600000000000002, -0.2617, -0.3337, -0.4114, -0.49520000000000003, -0.6128, -0.7412, -0.8893, -1.0576, -1.1963, -1.3078, -1.3467, -1.3878, -1.3582999999999998, -1.3092, -1.2695, -1.228, -1.1945000000000001, -1.1601, -1.1042, -1.059, -0.9866999999999999, -0.9206000000000001, -0.8498, -0.7771, -0.715, -0.6479, -0.5662, -0.48310000000000003, -0.39039999999999997, -0.32010000000000005, -0.28290000000000004, -0.25129999999999997, -0.25839999999999996, -0.2653, -0.26580000000000004, -0.23620000000000002, -0.2011, -0.1655, -0.1225, -0.08979999999999999, -0.0868, -0.0887, -0.08979999999999999, -0.0054, -0.0009, 0.0097, 0.0299, 0.0421, 0.0638, 0.0904, 0.1054, 0.125, 0.1579, 0.1819, 0.2085, 0.2373, 0.2589, 0.2678, 0.2813, 0.2952, 0.3031, 0.3042, 0.3201, 0.328, 0.3381, 0.3434, 0.3531, 0.3539, 0.3493, 0.3355, 0.3246, 0.304, 0.2853, 0.2659, 0.2314, 0.2004, 0.1645, 0.1244, 0.0905, 0.061, 0.0348, 0.0098, -0.0125, -0.0152, -0.0363, -0.0487, -0.0695, -0.0824, -0.1029, -0.112, -0.1182, -0.1034, -0.1091, -0.1058, -0.0981, -0.0959, -0.0955, -0.0875, -0.0785, -0.0711, -0.0806, -0.0799, -0.0833, -0.0906]
    #
    # eight =[0.152, 0.1615, 0.1777, 0.19069999999999998, 0.20820000000000002, 0.2143, 0.2165, 0.2267, 0.23340000000000002, 0.248, 0.2344, 0.21409999999999996, 0.2012, 0.20329999999999998, 0.20500000000000002, 0.17440000000000005, 0.1592, 0.10799999999999998, 0.055400000000000005, 0.024500000000000077, 0.00019999999999997797, -0.03660000000000002, -0.06530000000000002, -0.09970000000000001, -0.14400000000000002, -0.20240000000000002, -0.2743, -0.3499, -0.4486, -0.5636, -0.6926, -0.8714999999999999, -1.0741, -1.3195000000000001, -1.6017000000000001, -1.8697, -2.1211, -2.1547, -2.2086, -2.0275, -1.8634, -1.7953, -1.7232999999999998, -1.6486, -1.5744, -1.4743, -1.3846, -1.2696, -1.1649, -1.0602, -0.9583999999999999, -0.8691, -0.7764, -0.6716, -0.5703, -0.4558, -0.3754, -0.3276, -0.2631, -0.2586, -0.25739999999999996, -0.2612, -0.2317, -0.1883, -0.1451, -0.097, -0.0611, -0.058800000000000005, -0.0625, -0.0636, 0.0182, 0.0204, 0.0302, 0.0502, 0.0597, 0.0794, 0.1067, 0.1186, 0.138, 0.1709, 0.1889, 0.2119, 0.2388, 0.2586, 0.2668, 0.2789, 0.2907, 0.2979, 0.2971, 0.3131, 0.3239, 0.3327, 0.3373, 0.3443, 0.3436, 0.3384, 0.3276, 0.3176, 0.2965, 0.2786, 0.2568, 0.2189, 0.1859, 0.1455, 0.1012, 0.0646, 0.0338, 0.0074, -0.0175, -0.0415, -0.0405, -0.0564, -0.0683, -0.086, -0.0962, -0.1076, -0.1118, -0.116, -0.1039, -0.1077, -0.1024, -0.0935, -0.086, -0.0848, -0.0758, -0.0652, -0.0595, -0.0712, -0.0738, -0.0818, -0.0925]
    # #
    # listy_two = [five,six,seven,eight ]
    # for i,j in zip(listy_two,listy_one):
    #     merge_data_new(i,j)

    # #绘制第一个场面的图片
    function_encapsulation(list_propotion_one_Lock_sjz,list_propotion_two_Lock_sjz,list_propotion_three_Lock_sjz ,
                           list_SJZ_xticks,
                           # list_propotion_one_Lock_xian, list_propotion_two_Lock_xian, list_propotion_three_Lock_xian,
                           # list_propotion_one_Lock_qqhe, list_propotion_two_Lock_qqhe, list_propotion_three_Lock_qqhe,
                           [-l for l in list_propotion_one_Lock_qqhe],
                           [-l for l in list_propotion_two_Lock_qqhe],
                             [-l for l in list_propotion_three_Lock_qqhe],
                           listXData_contrast_qqhe)

    # 绘制第二个场面的图片
    #[-l for l in list_propotion_one_contrast_sjz], [-l for l in list_propotion_two_contrast_sjz],
    #[-l for l in list_propotion_three_contrast_sjz], [-l for l in list_propotion_four_contrast_sjz],

    second_one = [ 0.0459, 0.1107, 0.1571, 0.2147, 0.2438, 0.2944, 0.3352, 0.3891, 0.4392, 0.473, 0.4921, 0.5113, 0.5383, 0.5638, 0.5685, 0.5743, 0.5783, 0.576, 0.58, 0.5707, 0.5559, 0.5411, 0.525, 0.4997, 0.4772, 0.454, 0.4369, 0.4081, 0.3887, 0.3217, 0.2525, 0.2065, 0.1696, 0.1191, 0.0771, 0.0453, 0.016, -0.0063, -0.0184, -0.0448, -0.0738, -0.0627, -0.0517, -0.0453, -0.0514, -0.0572, -0.0738, -0.1087, -0.1268, -0.1689, -0.2367, -0.2177, -0.1851, -0.1519, -0.1332, -0.0904, -0.0905, -0.1123, -0.1351, -0.1609, -0.1846, -0.1751, -0.1629, -0.1718, -0.1357, -0.1108, -0.0936, -0.0734, -0.0403, -0.0013, 0.0254, 0.0698, 0.1188, 0.1429, 0.1515, 0.1464, 0.1465, 0.146, 0.1641, 0.1829, 0.2061, 0.2266, 0.2414, 0.2405, 0.2316, 0.2351, 0.1922, 0.1593, 0.1442, 0.1272, 0.1136, 0.0945, 0.0813, 0.0664, 0.0512, 0.0323,-0.0286, -0.0331, -0.0474, -0.0476, -0.0513, -0.064, -0.0938, -0.0799, -0.0612, -0.0877, -0.1257, -0.1022, -0.0916, -0.0921, -0.0706, -0.0641, -0.0511, -0.0264, 0.0048]
    second_two = [ 0.0563, 0.0822, 0.1192, 0.1364, 0.1698, 0.1951, 0.2339, 0.2697, 0.2989, 0.3228, 0.3454, 0.3719, 0.3892, 0.4058, 0.4245, 0.4398, 0.4404, 0.4364, 0.4247, 0.4028, 0.3785, 0.3674, 0.3395, 0.3241, 0.3041, 0.2968, 0.2805, 0.2646, 0.2262, 0.1835, 0.1442, 0.1127, 0.0718, 0.0478, 0.0333, 0.019, 0.0, -0.0141, -0.0235, -0.0329, -0.0186, 0.0046, 0.0138, 0.0046, -0.0094, -0.0335, -0.0534, -0.0788, -0.1162, -0.1495, -0.151, -0.1354, -0.1198, -0.1036, -0.0663, -0.0773, -0.0938, -0.1105, -0.1277, -0.139, -0.139, -0.139, -0.1559, -0.1543, -0.1361, -0.125, -0.0979, -0.0609, -0.0352, -0.01, 0.0294, 0.0583, 0.0769, 0.0813, 0.09, 0.0896, 0.0841, 0.106, 0.1193, 0.1324, 0.1455, 0.15, 0.15, 0.1461, 0.1584, 0.1455, 0.1279, 0.1193, 0.106, 0.0922, 0.0787, 0.0694, 0.0556, 0.0463, 0.037,-0.0451, -0.0451, -0.0455, -0.0227, -0.0153, -0.0308, -0.0465, -0.0469, -0.0472, -0.064, -0.0806, -0.0976, -0.0984, -0.1157, -0.1148, -0.0968, -0.0794, -0.0543, -0.015, 0.0074]

    second_three = [ 0.036, 0.0839, 0.1184, 0.1616, 0.1854, 0.2254, 0.2584, 0.3004, 0.3448, 0.376, 0.3964, 0.4156, 0.4408, 0.4638, 0.4705, 0.4756, 0.4799, 0.4791, 0.48, 0.4696, 0.4537, 0.4376, 0.4236, 0.4017, 0.3828, 0.3629, 0.3477, 0.3226, 0.305, 0.2551, 0.2007, 0.162, 0.1287, 0.0863, 0.0521, 0.0277, 0.0046, -0.0138, -0.0252, -0.0461, -0.0671, -0.0586, -0.048, -0.0422, -0.0481, -0.0541, -0.0675, -0.0923, -0.1063, -0.1355, -0.1807, -0.1709, -0.1481, -0.1216, -0.102, -0.0663, -0.0654, -0.081, -0.0961, -0.1127, -0.1266, -0.1186, -0.1104, -0.1167, -0.0938, -0.0748, -0.0594, -0.0407, -0.0142, 0.0152, 0.0368, 0.0714, 0.1085, 0.129, 0.1376, 0.1336, 0.1336, 0.1321, 0.1454, 0.1602, 0.1778, 0.1932, 0.2045, 0.2041, 0.1986, 0.2025, 0.1727, 0.1473, 0.1343, 0.1192, 0.1075, 0.093, 0.0824, 0.0686, 0.055, 0.0382,-0.0446, -0.0467, -0.0533, -0.0495, -0.0477, -0.0632, -0.0855, -0.0815, -0.0711, -0.0895, -0.1173, -0.105, -0.0909, -0.0903, -0.074, -0.0604, -0.045, -0.022, 0.0058]
    second_four = [ 0.0904, 0.1334, 0.1883, 0.2183, 0.2654, 0.3032, 0.3503, 0.4035, 0.4421, 0.4699, 0.4936, 0.5229, 0.5488, 0.5573, 0.5636, 0.5715, 0.5718, 0.5692, 0.5568, 0.5366, 0.5156, 0.4969, 0.4702, 0.4473, 0.4219, 0.4019, 0.3713, 0.3484, 0.2938, 0.2312, 0.1863, 0.1407, 0.0878, 0.0471, 0.0177, -0.0102, -0.0369, -0.0563, -0.083, -0.1076, -0.0977, -0.0848, -0.0775, -0.0844, -0.0932, -0.11, -0.1381, -0.1549, -0.1893, -0.243, -0.2314, -0.2029, -0.1698, -0.1361, -0.0852, -0.0828, -0.0988, -0.1151, -0.1306, -0.1448, -0.1352, -0.1252, -0.133, -0.1057, -0.0836, -0.0651, -0.0405, -0.0085, 0.025, 0.0513, 0.0915, 0.1348, 0.1571, 0.1668, 0.1618, 0.1591, 0.1521, 0.165, 0.1798, 0.1975, 0.2121, 0.2247, 0.2237, 0.2177, 0.2219, 0.1884, 0.1615, 0.1477, 0.1304, 0.1171, 0.1009, 0.0887, 0.072, 0.0554, 0.0359,-0.0837, -0.0835, -0.0886, -0.0772, -0.0742, -0.1048, -0.1451, -0.1519, -0.1473, -0.178, -0.2263, -0.2141, -0.1866, -0.1922, -0.1679, -0.1353, -0.1053, -0.0632, -0.016, 0.0276]

    second_five =[-0.0786, -0.0684, -0.0578, -0.0404, -0.0136, 0.0299, 0.0576, 0.0858, 0.1042, 0.131, 0.1627, 0.1998, 0.2193, 0.2502, 0.2626, 0.2666, 0.2756, 0.3211, 0.3639, 0.3971, 0.4082, 0.4074, 0.3723, 0.3325, 0.3163, 0.2899, 0.2646, 0.2291, 0.2004, 0.176, 0.1757, 0.1666, 0.1323, 0.096, 0.0675, 0.0353, 0.0175, 0.009, 0.0043, 0.0182, 0.0321, 0.0494, 0.0554, 0.0572, 0.0449, 0.0206, 0.0215, 0.0074, -0.0031, -0.0129, -0.0237, -0.0348, -0.0387, -0.0269, -0.0413, -0.0536, -0.0679, -0.0824, -0.0945, -0.098, -0.0909, -0.0995, -0.0962, -0.1, -0.0998, -0.098, -0.0912, -0.0631, -0.0615, -0.0543, -0.0391, 0.0108, 0.02, 0.0437, 0.0773, 0.1457, 0.211, 0.2632, 0.2996, 0.3464, 0.3886, 0.4093, 0.4229, 0.4166, 0.4099, 0.399, 0.3897, 0.3804, 0.3689, 0.3617, 0.3513, 0.3399, 0.33, 0.3148, 0.3042, 0.2794, 0.2643, 0.2234, 0.1785, 0.1375, 0.1034, 0.0554, 0.0087, -0.0159, -0.0385, -0.0414, -0.0462, -0.0415, -0.0456, -0.0453, -0.0358,-0.0395, -0.0491, -0.0735, -0.0945, -0.1245, -0.1344, -0.155, -0.1713, -0.1744, -0.17, -0.1526, -0.1401, -0.1159, -0.0975, -0.0787, -0.0622, -0.0454, -0.031, -0.0268, -0.0097]

    second_six= [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0091, 0.0152, 0.0182, 0.0212, 0.0212, 0.0212, 0.0212, 0.0212, 0.0212, 0.0212, 0.0212, 0.0212, 0.0212, 0.0212, 0.0212, 0.0212, 0.0212, 0.0212, 0.0212, 0.0212, 0.0212, 0.0212, 0.0031, -0.0092, -0.0154, -0.0217, -0.0217, -0.0217, -0.0217, -0.0217, -0.0217, -0.0217, -0.0217, -0.0217, -0.0217, -0.0217, -0.0217, -0.0217, -0.0217, -0.0217, -0.0217, -0.0217, -0.0217, -0.0217, -0.0123, -0.0061, -0.003, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    second_seven= [-0.0368, -0.0282, -0.0198, -0.0033, 0.0234, 0.0576, 0.0847, 0.1115, 0.1282, 0.153, 0.1798, 0.2037, 0.2178, 0.2389, 0.2422, 0.2427, 0.246, 0.2764, 0.298, 0.3143, 0.3197, 0.3145, 0.2871, 0.2568, 0.2418, 0.2195, 0.1969, 0.1699, 0.1467, 0.1275, 0.1252, 0.1144, 0.0901, 0.0665, 0.046, 0.0245, 0.0121, 0.0064, 0.0014, 0.016, 0.0254, 0.0373, 0.0424, 0.0429, 0.033, 0.0136, 0.0115, -0.0007, -0.0089, -0.0164, -0.0241, -0.031, -0.0337, -0.0281, -0.0386, -0.0478, -0.0593, -0.0695, -0.0797, -0.0826, -0.0796, -0.086, -0.0851, -0.0894, -0.09, -0.0882, -0.0829, -0.0626,  0.0097, 0.0168, 0.0324, 0.0511, 0.0616, 0.0809, 0.1076, 0.1559, 0.202, 0.2415, 0.2696, 0.3054, 0.338, 0.356, 0.3705, 0.3627, 0.3573, 0.3481, 0.3385, 0.3283, 0.3192, 0.3107, 0.2989, 0.2879, 0.2758, 0.2602, 0.2483, 0.2252, 0.2111, 0.1787, 0.1424, 0.1075, 0.0793, 0.0428, 0.0089, -0.0118, -0.0353, -0.0344, -0.0391, -0.0363, -0.0381, -0.0372, -0.0325,-0.0597, -0.0538, -0.0426, -0.0418, -0.0484, -0.0642, -0.0757, -0.0945, -0.0995, -0.1111, -0.1206, -0.1215, -0.1183, -0.1017, -0.09, -0.0708, -0.0531, -0.0349, -0.02, -0.0045]

    second_eight= [-0.0263, -0.0149, -0.0043, 0.0165, 0.0501, 0.0907, 0.1243, 0.1581, 0.1804, 0.2119, 0.2484, 0.2758, 0.2945, 0.3219, 0.3271, 0.3267, 0.3287, 0.359, 0.3748, 0.3836, 0.3834, 0.3716, 0.3368, 0.299, 0.2789, 0.2517, 0.2234, 0.1918, 0.1649, 0.1432, 0.1392, 0.1256,0.0969, 0.0708, 0.0463, 0.0212, 0.0067, 0.0006, 0.0063, 0.0246, 0.0318, 0.0426, 0.0469, 0.0459, 0.0347, 0.0127, 0.0093, -0.0036, -0.0127, -0.021, -0.029, -0.036, -0.0384, -0.0337, -0.0458, -0.0566, -0.0707, -0.0833, -0.0947, -0.0978, -0.0959, -0.1047, -0.1038, -0.1099, -0.1109, -0.109, -0.1032, 0.0032, 0.021, 0.0309, 0.0499, 0.0728, 0.0866, 0.1086, 0.1391, 0.1912, 0.2415, 0.2843, 0.3149, 0.3529, 0.3886, 0.4087, 0.4261, 0.4179, 0.4134, 0.4044, 0.3941, 0.383, 0.3743, 0.3644, 0.3508, 0.3387, 0.3241, 0.306, 0.2919, 0.2651, 0.2491, 0.2138, 0.1721, 0.1304, 0.0971, 0.055, 0.0144, -0.0116, -0.0426, -0.0406, -0.0476, -0.0454, -0.0468, -0.0458, -0.0423, -0.0809, -0.0773, -0.0718, -0.0595, -0.058, -0.0651, -0.0818, -0.0941, -0.1134, -0.1176, -0.1282, -0.1378, -0.1374, -0.1341, -0.1144, -0.1008, -0.0776, -0.056, -0.0335, -0.0156]

    # terre=[]
    # for i in range(len(eeee)):
    #     if i <=36:
    #         terre.append(-eeee[i])
    #     else:
    #         terre.append(eeee[i])
    # print(terre)
    # print(len(terre))

    # # 绘制第二个场面的图片
    # function_encapsulation(
    #    #  list_propotion_one_contrast_sjz,list_propotion_two_contrast_sjz,
    #    # list_propotion_three_contrast_sjz,list_propotion_four_contrast_sjz,
    #    #  [-l for l in list(reversed(list_propotion_one_contrast_sjz))], [-l for l in (reversed(list_propotion_two_contrast_sjz))],
    #    #  [-l for l in list(reversed(list_propotion_three_contrast_sjz))], [-l for l in list(reversed(list_propotion_four_contrast_sjz))],
    #    #  list(reversed(list_propotion_one_contrast_sjz)),list(reversed(list_propotion_two_contrast_sjz)),
    #    #  list(reversed(list_propotion_three_contrast_sjz)),list(reversed(list_propotion_four_contrast_sjz)),
    #    second_one,second_three,second_four,
    #    list_SJZ_xticks,
    #     # list_propotion_one_Lock_xian, list_propotion_two_Lock_xian, list_propotion_three_Lock_xian,
    #     # list_propotion_four_Lock_xian,
    #    # list_propotion_one_contrast_xian, list_propotion_two_contrast_xian, list_propotion_three_contrast_xian, list_propotion_four_contrast_xian,
    #    second_five,second_seven,second_eight,
#    list_xian_xticks)


    list_avrage_node= [0.0303, 0.003599999999999992, -0.0015000000000000013, -0.021800000000000014, -0.012299999999999978, -0.03959999999999997, -0.02639999999999998, -0.04780000000000001, -0.057599999999999985, -0.03019999999999995, 0.0353, 0.04949999999999999, 0.06259999999999999, 0.06290000000000007, 0.044399999999999995, 0.05819999999999992, 0.05740000000000001, 0.057800000000000074, 0.039000000000000035, 0.02959999999999996, 0.024600000000000066, 0.016100000000000003, 0.006699999999999928, -0.00029999999999996696, -0.015300000000000036, -0.031299999999999994, -0.05970000000000003, -0.07880000000000004, -0.1271, -0.12539999999999998, -0.1164, -0.16099999999999998, -0.27, -0.3192, -0.4198, -0.5623, -0.6074, -0.7583, -0.868, -0.9387000000000001, -0.9519000000000001, -0.9815, -0.9986, -1.0076, -0.9675999999999999, -0.955, -0.9216, -0.8664999999999999, -0.8297, -0.7506999999999999, -0.6343, -0.596, -0.6408, -0.6625, -0.6913, -0.7244999999999999, -0.6965, -0.5582, -0.4326, -0.34500000000000003, -0.2474, -0.20049999999999998, -0.17099999999999999, -0.1432, -0.17070000000000002, -0.1889, -0.22659999999999997, -0.20989999999999998, -0.21150000000000002, -0.2146, -0.20170000000000002, -0.21660000000000001, -0.2576, -0.29359999999999997, -0.27690000000000003, -0.2792, -0.25579999999999997, -0.2501, -0.2657, -0.3087, -0.3784, -0.3582, -0.3374, -0.3698, -0.38, -0.3823, -0.333720000000000003, -0.3616, -0.34450000000000003, -0.3341, -0.3176, -0.3151, -0.3193, -0.32, -0.3048, -0.2619, -0.2066, -0.1749, -0.1561, -0.1401, -0.1266, -0.09659999999999999, -0.0020000000000000018, -0.0007000000000000062, 0.012399999999999994, 0.091, 0.1565, 0.1312, 0.0884, 0.0604, 0.009799999999999996, -0.015199999999999991, -0.06440000000000001, -0.0998, -0.1324]

    #使用公历/农历时间减去正常时间段后绘制的对比图    绘制第三个场面的图片
    # function_encapsulation(
    #                        #  merge_data(list_propotion_one_Lock_sjz,[-l for l in list_propotion_one_contrast_sjz][0:30]),
    #                        # merge_data(list_propotion_two_Lock_sjz,[-l for l in list_propotion_two_contrast_sjz][0:30]),
    #                        # merge_data(list_propotion_three_Lock_sjz, [-l for l in list_propotion_three_contrast_sjz][0:30]),
    #                        # merge_data(list_propotion_four_Lock_sjz,[-l for l in list_propotion_four_contrast_sjz][0:30]),
    #
    #                      # merge_data(list_propotion_one_Lock_sjz,second_one),
    #                     # merge_data(list_propotion_two_Lock_sjz,second_two),
    #                     list_avrage_node,
    #                     merge_data(list_propotion_two_Lock_sjz, second_three),
    #                     merge_data(list_propotion_three_Lock_sjz,second_four),
    #                        list_SJZ_xticks,
    #                        merge_data(list_propotion_one_Lock_xian, second_five),
    #                       # merge_data(list_propotion_two_Lock_xian, second_six),
    #                       merge_data(list_propotion_two_Lock_xian, second_seven),
    #                       merge_data(list_propotion_three_Lock_xian, second_eight),
    #                        list_xian_xticks)






    one =  [0.015300000000000001, 0.0812, 0.1086, 0.125, 0.14690000000000003, 0.14629999999999999, 0.1547, 0.1575, 0.1651, 0.20410000000000003, 0.22139999999999993, 0.19129999999999997, 0.14339999999999997, 0.13759999999999994, 0.09130000000000005, 0.07379999999999998, 0.06340000000000001, 0.0475000000000001, 0.02169999999999994, -0.008199999999999985, -0.02939999999999998, -0.058499999999999996, -0.059699999999999975, -0.05930000000000002, -0.07340000000000002, -0.09670000000000001, -0.13689999999999997, -0.17700000000000005, -0.22060000000000002, -0.2631, -0.2811, -0.3758, -0.4762, -0.5701999999999999, -0.7057, -0.8827, -0.9602999999999999, -1.0917000000000001, -1.2046000000000001, -1.3146, -1.3879000000000001, -1.3969, -1.4084, -1.3904, -1.3687, -1.3968, -1.4174, -1.3808, -1.3395, -1.282, -1.2362, -1.2032, -1.2384, -1.2002, -1.194, -1.1420000000000001, -1.0646, -0.8912, -0.7588, -0.7058, -0.6605, -0.6167999999999999, -0.5511, -0.4987, -0.448, -0.4142, -0.4147, -0.3835, -0.3473, -0.32030000000000003, -0.1682, -0.1348, -0.1238, -0.1037, -0.0736, -0.0566, -0.0302, -0.0112, -0.003, -0.015, -0.0468, -0.0574, -0.0792, -0.1088, -0.1383, -0.159, -0.1701, -0.1698, -0.1432, -0.1327, -0.131, -0.1401, -0.1508, -0.1602, -0.1553, -0.1458, -0.1458, -0.133, -0.1347, -0.1394, -0.1359, -0.1325, -0.0808, -0.0622, -0.0192, 0.0312, 0.0746, 0.0931, 0.0862, 0.0675, 0.0312, -0.0036, -0.0419, -0.063, -0.0729]

    two =  [0.1678, 0.22089999999999999, 0.2699, 0.3226, 0.36819999999999997, 0.42510000000000003, 0.4839, 0.5014, 0.505, 0.5164, 0.5083, 0.4902, 0.4799999999999999, 0.5121, 0.5152, 0.5273000000000001, 0.49970000000000003, 0.4473, 0.4111, 0.4007, 0.38210000000000005, 0.3544, 0.35469999999999996, 0.32919999999999994, 0.2881, 0.25730000000000003, 0.18670000000000003, 0.11159999999999998, 0.020600000000000007, -0.08519999999999997, -0.1911, -0.3607, -0.5438000000000001, -0.7733, -1.0698, -1.5419, -1.9539, -2.8701000000000003, -3.4128000000000003, -3.5380000000000003, -3.4391000000000003, -3.2177000000000002, -3.013, -2.8279, -2.6343, -2.4362000000000004, -2.2685, -2.1293, -1.8881999999999999, -1.6886999999999999, -1.4933, -1.3477000000000001, -1.3074000000000001, -1.2539, -1.2325, -1.2034, -1.1474, -1.0073, -0.8586, -0.7978999999999999, -0.7376, -0.6987, -0.6257, -0.5596, -0.5206999999999999, -0.4891, -0.49479999999999996, -0.4506, -0.4048, -0.3553, -0.3, -0.2701, -0.2614, -0.2402, -0.2065, -0.1799, -0.1546, -0.1256, -0.1034, -0.098, -0.1078, -0.0918, -0.081, -0.0802, -0.0845, -0.0939, -0.0935, -0.093, -0.0685, -0.0591, -0.0498, -0.0498, -0.0498, -0.0498, -0.0541, -0.0541, -0.0541, -0.0493, -0.0402, -0.0402, -0.0402, -0.0402, -0.0221, -0.0221, -0.0132, 0.0044, 0.0216, 0.03, 0.0299, 0.0298, 0.0171, 0.0043, -0.0086, -0.0172, -0.0259]

    three = [0.0451, 0.05070000000000001, 0.0688, 0.0859, 0.10659999999999999, 0.1092, 0.1182, 0.12310000000000001, 0.13299999999999998, 0.16319999999999998, 0.17959999999999998, 0.16670000000000001, 0.1476, 0.14990000000000003, 0.1174, 0.1099, 0.10369999999999996, 0.09210000000000002, 0.0746, 0.057699999999999974, 0.046599999999999975, 0.027600000000000013, 0.02460000000000001, 0.020399999999999974, 0.0030999999999999917, -0.02100000000000002, -0.05660000000000004, -0.089, -0.12550000000000003, -0.1583, -0.17310000000000003, -0.2323, -0.29469999999999996, -0.3557, -0.4411, -0.5449999999999999, -0.5932, -0.6738, -0.7405, -0.8026, -0.8495, -0.8615, -0.879, -0.8798, -0.8793, -0.8981, -0.9094, -0.8912, -0.8642000000000001, -0.8305, -0.8010999999999999, -0.7816, -0.8136, -0.8002, -0.7976000000000001, -0.7692, -0.7184, -0.619, -0.5355, -0.5036, -0.476, -0.44920000000000004, -0.4071, -0.3712, -0.333, -0.3076, -0.3045, -0.2833, -0.2591, -0.2394, -0.1371, -0.1149, -0.1071, -0.0936, -0.0683, -0.0526, -0.0314, -0.015, -0.0079, -0.0149, -0.0339, -0.0399, -0.0518, -0.0688, -0.0859, -0.0978, -0.1045, -0.1029, -0.085, -0.0801, -0.0804, -0.0865, -0.0939, -0.0991, -0.0967, -0.0896, -0.0896, -0.0814, -0.0824, -0.0855, -0.0833, -0.0812, -0.0501, -0.0384, -0.0123, 0.0187, 0.046, 0.0582, 0.0559, 0.0448, 0.0216, 0.0009, -0.0218, -0.0344, -0.0407]

    four =  [0.0387, 0.042699999999999995, 0.06259999999999999, 0.08159999999999999, 0.10700000000000001, 0.1085, 0.11400000000000002, 0.1139, 0.1187, 0.1462, 0.15389999999999998, 0.13279999999999997, 0.10370000000000007, 0.10679999999999995, 0.07549999999999996, 0.06860000000000005, 0.060699999999999976, 0.04700000000000004, 0.03400000000000003, 0.025000000000000022, 0.02750000000000008, 0.019999999999999962, 0.02739999999999998, 0.032799999999999996, 0.020999999999999963, -0.0015000000000000013, -0.038000000000000034, -0.06769999999999998, -0.10449999999999998, -0.1351, -0.1439, -0.19889999999999997, -0.26189999999999997, -0.3301, -0.4335, -0.5602, -0.6191, -0.7262, -0.8055, -0.889, -0.967, -0.9976, -1.0408, -1.0598, -1.0745, -1.1031, -1.1185, -1.0968, -1.0613000000000001, -1.0236, -0.9893000000000001, -0.9674, -1.0212, -1.0278, -1.0389, -1.0153, -0.9527000000000001, -0.8254, -0.7071, -0.6596, -0.621, -0.5811000000000001, -0.522, -0.4735, -0.4204, -0.385, -0.3751, -0.3465, -0.3116, -0.2851, -0.178, -0.1518, -0.138, -0.1219, -0.0902, -0.0686, -0.0423, -0.021, -0.0108, -0.0164, -0.0355, -0.0395, -0.0498, -0.0668, -0.0844, -0.0977, -0.1045, -0.1019, -0.0838, -0.0796, -0.0813, -0.0877, -0.0954, -0.1, -0.0995, -0.0908, -0.0904, -0.0822, -0.0833, -0.0861, -0.0843, -0.0825, -0.0509, -0.0406, -0.0143, 0.0183, 0.0473, 0.0623, 0.0586, 0.0458, 0.0224, 0.0019, -0.0202, -0.0332, -0.0397]
    #



    five =  [-0.010100000000000001, 0.0773, 0.1064, 0.1247, 0.1491, 0.16310000000000002, 0.175, 0.18860000000000002, 0.19960000000000003, 0.21559999999999999, 0.19879999999999998, 0.172, 0.1432, 0.13329999999999997, 0.11680000000000001, 0.08779999999999999, 0.07419999999999993, 0.03920000000000001, -0.00550000000000006, -0.051899999999999946, -0.09209999999999996, -0.1301, -0.14919999999999994, -0.18059999999999998, -0.20080000000000003, -0.24380000000000002, -0.2980999999999999, -0.36050000000000004, -0.4409, -0.52, -0.6102000000000001, -0.7545999999999999, -0.911, -1.1006, -1.3441, -1.5327000000000002, -1.6772, -1.7381, -1.8168000000000002, -1.7979, -1.7492, -1.6605999999999999, -1.583, -1.546, -1.5038, -1.4127, -1.3762, -1.2713, -1.2007, -1.1093, -1.0165, -0.9414, -0.8583000000000001, -0.7516, -0.6425000000000001, -0.5207, -0.4208, -0.3708, -0.3404, -0.3639, -0.3786, -0.3875, -0.3443, -0.3035, -0.2666, -0.2131, -0.17109999999999997, -0.1717, -0.1732, -0.1749, -0.0446, -0.0329, -0.0136, 0.0184, 0.0367, -0.0238, 0.0252, 0.06780000000000001, 0.11069999999999999, 0.14040000000000002, 0.1798, 0.2278, 0.2815, 0.32589999999999997, 0.34540000000000004, 0.3449, 0.32930000000000004, 0.3016, 0.2894, 0.3081, 0.324, 0.3414, 0.3434, 0.3416, 0.3492, 0.3302, 0.3173, 0.31179999999999997, 0.3075, 0.30179999999999996, 0.2919, 0.28780000000000006, 0.2566, 0.2219, 0.1783, 0.1765, 0.1346, 0.1079, 0.0795, 0.0664, 0.0757, 0.0508, 0.0352, 0.0191, -0.0011, -0.02, -0.0431, -0.0565, -0.0365, -0.0567, -0.0631, -0.0656, -0.0754, -0.0853, -0.0819, -0.0818, -0.0726, -0.0974, -0.0929, -0.1192, -0.151]

    six = [0.10400000000000001, 0.159, 0.1913, 0.2318, 0.2671, 0.3168, 0.363, 0.3715, 0.3665, 0.3593, 0.34230000000000005, 0.32170000000000004, 0.33559999999999995, 0.3692, 0.3853, 0.3793, 0.3548, 0.296, 0.25639999999999996, 0.23879999999999996, 0.2021, 0.15140000000000003, 0.1325, 0.09309999999999996, 0.04660000000000003, 0.008199999999999985, -0.06940000000000002, -0.1565, -0.2464, -0.3539, -0.4739, -0.621, -0.795, -1.0078, -1.288, -1.5969000000000002, -1.863, -2.1718, -2.3948, -2.424, -2.3831, -2.27, -2.064, -1.8434, -1.6872, -1.5489, -1.4425, -1.322, -1.1582999999999999, -1.0035, -0.8779, -0.7657999999999999, -0.6759000000000001, -0.5791999999999999, -0.4961, -0.41209999999999997, -0.3341, -0.27599999999999997, -0.24309999999999998, -0.1995, -0.1661, -0.1386, -0.1084, -0.08750000000000001, -0.0819, -0.084, -0.0822, -0.0683, -0.05059999999999999, -0.039400000000000004, -0.0154, -0.0154, -0.0154, -0.0154, -0.0092, -0.011000000000000001, -0.0048000000000000004, -0.006700000000000001, 0.009499999999999998, 0.0359, 0.0579, 0.06490000000000001, 0.07680000000000001, 0.074, 0.08410000000000001, 0.0863, 0.0767, 0.0722, 0.0601, 0.0553, 0.055099999999999996, 0.0656, 0.061700000000000005, 0.056999999999999995, 0.0606, 0.0528, 0.0411, 0.03259999999999999, 0.02479999999999999, 0.005500000000000005, -0.01580000000000001, -0.03560000000000001, -0.057999999999999996, -0.0733, -0.0822, -0.0468, -0.0572, -0.0678, -0.0785, -0.0822, -0.0825, -0.0828, -0.0724, -0.0761, -0.0727, -0.0764, -0.0729, -0.0694, -0.0586, -0.055, -0.0444, -0.0339, -0.0235, -0.0033, 0.0065, 0.0194, 0.0289, 0.0383, 0.0414, 0.0476, 0.0538]

    seven =[0.0878, 0.1037, 0.1195, 0.1325, 0.1486, 0.15740000000000004, 0.1658, 0.18039999999999998, 0.19209999999999997, 0.20819999999999997, 0.20229999999999998, 0.19030000000000002, 0.19310000000000005, 0.19240000000000002, 0.18840000000000007, 0.16619999999999996, 0.15419999999999995, 0.12060000000000004, 0.07919999999999999, 0.046999999999999986, 0.017199999999999993, -0.018799999999999983, -0.04510000000000003, -0.07640000000000002, -0.10930000000000001, -0.15280000000000002, -0.20600000000000002, -0.2617, -0.3337, -0.4114, -0.49520000000000003, -0.6128, -0.7412, -0.8893, -1.0576, -1.1963, -1.3078, -1.3467, -1.3878, -1.3582999999999998, -1.3092, -1.2695, -1.228, -1.1945000000000001, -1.1601, -1.1042, -1.059, -0.9866999999999999, -0.9206000000000001, -0.8498, -0.7771, -0.715, -0.6479, -0.5662, -0.48310000000000003, -0.39039999999999997, -0.32010000000000005, -0.28290000000000004, -0.25129999999999997, -0.25839999999999996, -0.2653, -0.26580000000000004, -0.23620000000000002, -0.2011, -0.1655, -0.1225, -0.08979999999999999, -0.0868, -0.0887, -0.08979999999999999, -0.0054, -0.0009, 0.0097, 0.0299, 0.0421, 0.003699999999999995, 0.037899999999999996, 0.0648, 0.09570000000000001, 0.12090000000000001, 0.1471, 0.18109999999999998, 0.22, 0.24930000000000002, 0.26249999999999996, 0.2647, 0.2548, 0.24019999999999997, 0.23300000000000004, 0.2485, 0.26170000000000004, 0.2767, 0.2762, 0.2776, 0.28049999999999997, 0.2675, 0.2553, 0.2477, 0.2383, 0.2283, 0.2141, 0.1999, 0.1723, 0.1381, 0.1006, 0.0905, 0.061, 0.0348, 0.0098, -0.0125, -0.0152, -0.0363, -0.0487, -0.0695, -0.0824, -0.1029, -0.112, -0.1182, -0.1034, -0.1091, -0.1058, -0.0981, -0.0959, -0.0955, -0.0875, -0.0785, -0.0711, -0.0806, -0.0799, -0.0833, -0.0906]

    eight = [0.152, 0.1615, 0.1777, 0.19069999999999998, 0.20820000000000002, 0.2143, 0.2165, 0.2267, 0.23340000000000002, 0.248, 0.2344, 0.21409999999999996, 0.2012, 0.20329999999999998, 0.20500000000000002, 0.17440000000000005, 0.1592, 0.10799999999999998, 0.055400000000000005, 0.024500000000000077, 0.00019999999999997797, -0.03660000000000002, -0.06530000000000002, -0.09970000000000001, -0.14400000000000002, -0.20240000000000002, -0.2743, -0.3499, -0.4486, -0.5636, -0.6926, -0.8714999999999999, -1.0741, -1.3195000000000001, -1.6017000000000001, -1.8697, -2.1211, -2.1547, -2.2086, -2.0275, -1.8634, -1.7953, -1.7232999999999998, -1.6486, -1.5744, -1.4743, -1.3846, -1.2696, -1.1649, -1.0602, -0.9583999999999999, -0.8691, -0.7764, -0.6716, -0.5703, -0.4558, -0.3754, -0.3276, -0.2631, -0.2586, -0.25739999999999996, -0.2612, -0.2317, -0.1883, -0.1451, -0.097, -0.0611, -0.058800000000000005, -0.0625, -0.0636, 0.0182, 0.0204, 0.0302, 0.0502, 0.0597, 0.017799999999999996, 0.0522, 0.0754, 0.10670000000000002, 0.1323, 0.1524, 0.1831, 0.22060000000000002, 0.2488, 0.2608, 0.25949999999999995, 0.2459, 0.22949999999999998, 0.22059999999999996, 0.23679999999999998, 0.2524, 0.267, 0.26539999999999997, 0.2652, 0.26680000000000004, 0.25389999999999996, 0.2449, 0.2389, 0.22909999999999997, 0.22000000000000003, 0.20239999999999997, 0.184, 0.1544, 0.1147, 0.0726, 0.0646, 0.0338, 0.0074, -0.0175, -0.0415, -0.0405, -0.0564, -0.0683, -0.086, -0.0962, -0.1076, -0.1118, -0.116, -0.1039, -0.1077, -0.1024, -0.0935, -0.086, -0.0848, -0.0758, -0.0652, -0.0595, -0.0712, -0.0738, -0.0818, -0.0925]


    # five =  [-0.010100000000000001, 0.0773, 0.1064, 0.1247, 0.1491, 0.16310000000000002, 0.175, 0.18860000000000002, 0.19960000000000003, 0.21559999999999999, 0.19879999999999998, 0.172, 0.1432, 0.13329999999999997, 0.11680000000000001, 0.08779999999999999, 0.07419999999999993, 0.03920000000000001, -0.00550000000000006, -0.051899999999999946, -0.09209999999999996, -0.1301, -0.14919999999999994, -0.18059999999999998, -0.20080000000000003, -0.24380000000000002, -0.2980999999999999, -0.36050000000000004, -0.4409, -0.52, -0.6102000000000001, -0.7545999999999999, -0.911, -1.1006, -1.3441, -1.5327000000000002, -1.6772, -1.7381, -1.8168000000000002, -1.7979, -1.7492, -1.6605999999999999, -1.583, -1.546, -1.5038, -1.4127, -1.3762, -1.2713, -1.2007, -1.1093, -1.0165, -0.9414, -0.8583000000000001, -0.7516, -0.6425000000000001, -0.5207, -0.4208, -0.3708, -0.3404, -0.3639, -0.3786, -0.3875, -0.3443, -0.3035, -0.2666, -0.2131, -0.17109999999999997, -0.1717, -0.1732, -0.1749, -0.0446, -0.0329, -0.0136, 0.0184, 0.0367, -0.0238, 0.0252, 0.06780000000000001, 0.11069999999999999, 0.14040000000000002, 0.1798, 0.2278, 0.2815, 0.32589999999999997, 0.34540000000000004, 0.3449, 0.32930000000000004, 0.3016, 0.2894, 0.3081, 0.324, 0.3414, 0.3434, 0.3416, 0.3492, 0.4618, 0.4462, 0.4366, 0.4156, 0.3964, 0.3782, 0.341, 0.3046, 0.2677, 0.2198, 0.1765, 0.1346, 0.1079, 0.0795, 0.0664, 0.0757, 0.0508, 0.0352, 0.0191, -0.0011, -0.02, -0.0431, -0.0565, -0.0365, -0.0567, -0.0631, -0.0656, -0.0754, -0.0853, -0.0819, -0.0818, -0.0726, -0.0974, -0.0929, -0.1192, -0.151]
    #
    # six = [0.10400000000000001, 0.159, 0.1913, 0.2318, 0.2671, 0.3168, 0.363, 0.3715, 0.3665, 0.3593, 0.34230000000000005, 0.32170000000000004, 0.33559999999999995, 0.3692, 0.3853, 0.3793, 0.3548, 0.296, 0.25639999999999996, 0.23879999999999996, 0.2021, 0.15140000000000003, 0.1325, 0.09309999999999996, 0.04660000000000003, 0.008199999999999985, -0.06940000000000002, -0.1565, -0.2464, -0.3539, -0.4739, -0.621, -0.795, -1.0078, -1.288, -1.5969000000000002, -1.863, -2.1718, -2.3948, -2.424, -2.3831, -2.27, -2.064, -1.8434, -1.6872, -1.5489, -1.4425, -1.322, -1.1582999999999999, -1.0035, -0.8779, -0.7657999999999999, -0.6759000000000001, -0.5791999999999999, -0.4961, -0.41209999999999997, -0.3341, -0.27599999999999997, -0.24309999999999998, -0.1995, -0.1661, -0.1386, -0.1084, -0.08750000000000001, -0.0819, -0.084, -0.0822, -0.0683, -0.05059999999999999, -0.039400000000000004, -0.0154, -0.0154, -0.0154, -0.0154, -0.0092, -0.011000000000000001, -0.0048000000000000004, -0.006700000000000001, 0.009499999999999998, 0.0359, 0.0579, 0.06490000000000001, 0.07680000000000001, 0.074, 0.08410000000000001, 0.0863, 0.0767, 0.0722, 0.0601, 0.0553, 0.055099999999999996, 0.0656, 0.061700000000000005, 0.056999999999999995, 0.0606, 0.1273, 0.1159, 0.1074, 0.0957, 0.0839, 0.0629, 0.0319, 0.0097, -0.0131, -0.0298, -0.0468, -0.0572, -0.0678, -0.0785, -0.0822, -0.0825, -0.0828, -0.0724, -0.0761, -0.0727, -0.0764, -0.0729, -0.0694, -0.0586, -0.055, -0.0444, -0.0339, -0.0235, -0.0033, 0.0065, 0.0194, 0.0289, 0.0383, 0.0414, 0.0476, 0.0538]
    #
    # seven =[0.0878, 0.1037, 0.1195, 0.1325, 0.1486, 0.15740000000000004, 0.1658, 0.18039999999999998, 0.19209999999999997, 0.20819999999999997, 0.20229999999999998, 0.19030000000000002, 0.19310000000000005, 0.19240000000000002, 0.18840000000000007, 0.16619999999999996, 0.15419999999999995, 0.12060000000000004, 0.07919999999999999, 0.046999999999999986, 0.017199999999999993, -0.018799999999999983, -0.04510000000000003, -0.07640000000000002, -0.10930000000000001, -0.15280000000000002, -0.20600000000000002, -0.2617, -0.3337, -0.4114, -0.49520000000000003, -0.6128, -0.7412, -0.8893, -1.0576, -1.1963, -1.3078, -1.3467, -1.3878, -1.3582999999999998, -1.3092, -1.2695, -1.228, -1.1945000000000001, -1.1601, -1.1042, -1.059, -0.9866999999999999, -0.9206000000000001, -0.8498, -0.7771, -0.715, -0.6479, -0.5662, -0.48310000000000003, -0.39039999999999997, -0.32010000000000005, -0.28290000000000004, -0.25129999999999997, -0.25839999999999996, -0.2653, -0.26580000000000004, -0.23620000000000002, -0.2011, -0.1655, -0.1225, -0.08979999999999999, -0.0868, -0.0887, -0.08979999999999999, -0.0054, -0.0009, 0.0097, 0.0299, 0.0421, 0.003699999999999995, 0.037899999999999996, 0.0648, 0.09570000000000001, 0.12090000000000001, 0.1471, 0.18109999999999998, 0.22, 0.24930000000000002, 0.26249999999999996, 0.2647, 0.2548, 0.24019999999999997, 0.23300000000000004, 0.2485, 0.26170000000000004, 0.2767, 0.2762, 0.2776, 0.28049999999999997, 0.3493, 0.3355, 0.3246, 0.304, 0.2853, 0.2659, 0.2314, 0.2004, 0.1645, 0.1244, 0.0905, 0.061, 0.0348, 0.0098, -0.0125, -0.0152, -0.0363, -0.0487, -0.0695, -0.0824, -0.1029, -0.112, -0.1182, -0.1034, -0.1091, -0.1058, -0.0981, -0.0959, -0.0955, -0.0875, -0.0785, -0.0711, -0.0806, -0.0799, -0.0833, -0.0906]
    #
    # eight = [0.152, 0.1615, 0.1777, 0.19069999999999998, 0.20820000000000002, 0.2143, 0.2165, 0.2267, 0.23340000000000002, 0.248, 0.2344, 0.21409999999999996, 0.2012, 0.20329999999999998, 0.20500000000000002, 0.17440000000000005, 0.1592, 0.10799999999999998, 0.055400000000000005, 0.024500000000000077, 0.00019999999999997797, -0.03660000000000002, -0.06530000000000002, -0.09970000000000001, -0.14400000000000002, -0.20240000000000002, -0.2743, -0.3499, -0.4486, -0.5636, -0.6926, -0.8714999999999999, -1.0741, -1.3195000000000001, -1.6017000000000001, -1.8697, -2.1211, -2.1547, -2.2086, -2.0275, -1.8634, -1.7953, -1.7232999999999998, -1.6486, -1.5744, -1.4743, -1.3846, -1.2696, -1.1649, -1.0602, -0.9583999999999999, -0.8691, -0.7764, -0.6716, -0.5703, -0.4558, -0.3754, -0.3276, -0.2631, -0.2586, -0.25739999999999996, -0.2612, -0.2317, -0.1883, -0.1451, -0.097, -0.0611, -0.058800000000000005, -0.0625, -0.0636, 0.0182, 0.0204, 0.0302, 0.0502, 0.0597, 0.017799999999999996, 0.0522, 0.0754, 0.10670000000000002, 0.1323, 0.1524, 0.1831, 0.22060000000000002, 0.2488, 0.2608, 0.25949999999999995, 0.2459, 0.22949999999999998, 0.22059999999999996, 0.23679999999999998, 0.2524, 0.267, 0.26539999999999997, 0.2652, 0.26680000000000004, 0.3384, 0.3276, 0.3176, 0.2965, 0.2786, 0.2568, 0.2189, 0.1859, 0.1455, 0.1012, 0.0646, 0.0338, 0.0074, -0.0175, -0.0415, -0.0405, -0.0564, -0.0683, -0.086, -0.0962, -0.1076, -0.1118, -0.116, -0.1039, -0.1077, -0.1024, -0.0935, -0.086, -0.0848, -0.0758, -0.0652, -0.0595, -0.0712, -0.0738, -0.0818, -0.0925]



    # # # print(len(five))
    # function_encapsulation(one,two,three,four,
    #                        list_SJZ_xticks,
    #                         five,six,seven,eight,
    #                        # list_propotion_one_Lock_xian, list_propotion_two_Lock_xian, list_propotion_three_Lock_xian,
    #                        # list_propotion_four_Lock_xian,
    #                        list_xian_xticks)

    # list_xian_xticks = ['20211115', '20211116', '20211117', '20211118', '20211119', '20211120', '20211121', '20211122', '20211123', '20211124', '20211125', '20211126', '20211127', '20211128', '20211129', '20211130', '20211201', '20211202', '20211203', '20211204', '20211205', '20211206', '20211207', '20211208', '20211209', '20211210', '20211211', '20211212', '20211213', '20211214', '20211215', '20211216', '20211217', '20211218', '20211219', '20211220', '20211221', '20211222', '20211223', '20211224', '20211225', '20211226', '20211227', '20211228', '20211229', '20211230', '20211231', '20220101', '20220102', '20220103', '20220104', '20220105', '20220106', '20220107', '20220108', '20220109', '20220110', '20220111', '20220112', '20220113', '20220114', '20220115', '20220116', '20220117', '20220118', '20220119', '20220120', '20220121', '20220122', '20220123', '20220124', '20220125', '20220126', '20220127', '20220128', '20220129', '20220130', '20220131', '20220201', '20220202', '20220203', '20220204', '20220205', '20220206', '20220207', '20220208', '20220209', '20220210', '20220211', '20220212', '20220213', '20220214', '20220215', '20220216', '20220217', '20220218', '20220219', '20220220', '20220221', '20220222', '20220223', '20220224', '20220225', '20220226', '20220227', '20220228', '20220301', '20220302', '20220303', '20220304', '20220305', '20220306', '20220307', '20220308', '20220309', '20220310', '20220311', '20220312', '20220313', '20220314', '20220315', '20220316', '20220317', '20220318', '20220319', '20220320', '20220321', '20220322', '20220323', '20220324', '20220325']
    # print(len(list_xian_xticks))
    # print(len(getdaylist(20211123,20220402)))
# print(getdaylist(20211123,20220402))


# eeee =[0.0786, 0.0684, 0.0578, 0.0404, 0.0136, -0.0299, -0.0576, -0.0858, -0.1042, -0.131, -0.1627, -0.1998, -0.2193, -0.2502, -0.2626, -0.2666, -0.2756, -0.3211, -0.3639, -0.3971, -0.4082, -0.4074, -0.3723, -0.3325, -0.3163, -0.2899, -0.2646, -0.2291, -0.2004, -0.176, -0.1757, -0.1666, -0.1323, -0.096, -0.0675, -0.0353, -0.0175, -0.009, -0.0043, 0.0182, 0.0321, 0.0494, 0.0554, 0.0572, 0.0449, 0.0206, 0.0215, 0.0074, -0.0031, -0.0129, -0.0237, -0.0348, -0.0387, -0.0269, -0.0413, -0.0536, -0.0679, -0.0824, -0.0945, -0.098, -0.0909, -0.0995, -0.0962, -0.1, -0.0998, -0.098, -0.0912, -0.0631, -0.0615, -0.0543, -0.0391, -0.0395, -0.0491, -0.0735, -0.0945, -0.1245, -0.1344, -0.155, -0.1713, -0.1744, -0.17, -0.1526, -0.1401, -0.1159, -0.0975, -0.0787, -0.0622, -0.0454, -0.031, -0.0268, -0.0097, 0.0108, 0.02, 0.0437, 0.0773, 0.1457, 0.211, 0.2632, 0.2996, 0.3464, 0.3886, 0.4093, 0.4229, 0.4166, 0.4099, 0.399, 0.3897, 0.3804, 0.3689, 0.3617, 0.3513, 0.3399, 0.33, 0.3148, 0.3042, 0.2794, 0.2643, 0.2234, 0.1785, 0.1375, 0.1034, 0.0554, 0.0087, -0.0159, -0.0385, -0.0414, -0.0462, -0.0415, -0.0456, -0.0453, -0.0358]
#
# ffff= [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0091, 0.0152, 0.0182, 0.0212, 0.0212, 0.0212, 0.0212, 0.0212, 0.0212, 0.0212, 0.0212, 0.0212, 0.0212, 0.0212, 0.0212, 0.0212, 0.0212, 0.0212, 0.0212, 0.0212, 0.0212, 0.0212, 0.0031, -0.0092, -0.0154, -0.0217, -0.0217, -0.0217, -0.0217, -0.0217, -0.0217, -0.0217, -0.0217, -0.0217, -0.0217, -0.0217, -0.0217, -0.0217, -0.0217, -0.0217, -0.0217, -0.0217, -0.0217, -0.0217, -0.0123, -0.0061, -0.003, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
#
# gggg= [0.0368, 0.0282, 0.0198, 0.0033, -0.0234, -0.0576, -0.0847, -0.1115, -0.1282, -0.153, -0.1798, -0.2037, -0.2178, -0.2389, -0.2422, -0.2427, -0.246, -0.2764, -0.298, -0.3143, -0.3197, -0.3145, -0.2871, -0.2568, -0.2418, -0.2195, -0.1969, -0.1699, -0.1467, -0.1275, -0.1252, -0.1144, -0.0901, -0.0665, -0.046, -0.0245, -0.0121, -0.0064, -0.0014, 0.016, 0.0254, 0.0373, 0.0424, 0.0429, 0.033, 0.0136, 0.0115, -0.0007, -0.0089, -0.0164, -0.0241, -0.031, -0.0337, -0.0281, -0.0386, -0.0478, -0.0593, -0.0695, -0.0797, -0.0826, -0.0796, -0.086, -0.0851, -0.0894, -0.09, -0.0882, -0.0829, -0.0626, -0.0597, -0.0538, -0.0426, -0.0418, -0.0484, -0.0642, -0.0757, -0.0945, -0.0995, -0.1111, -0.1206, -0.1215, -0.1183, -0.1017, -0.09, -0.0708, -0.0531, -0.0349, -0.02, -0.0045, 0.0097, 0.0168, 0.0324, 0.0511, 0.0616, 0.0809, 0.1076, 0.1559, 0.202, 0.2415, 0.2696, 0.3054, 0.338, 0.356, 0.3705, 0.3627, 0.3573, 0.3481, 0.3385, 0.3283, 0.3192, 0.3107, 0.2989, 0.2879, 0.2758, 0.2602, 0.2483, 0.2252, 0.2111, 0.1787, 0.1424, 0.1075, 0.0793, 0.0428, 0.0089, -0.0118, -0.0353, -0.0344, -0.0391, -0.0363, -0.0381, -0.0372, -0.0325]
#
# hhhh= [0.0263, 0.0149, 0.0043, -0.0165, -0.0501, -0.0907, -0.1243, -0.1581, -0.1804, -0.2119, -0.2484, -0.2758, -0.2945, -0.3219, -0.3271, -0.3267, -0.3287, -0.359, -0.3748, -0.3836, -0.3834, -0.3716, -0.3368, -0.299, -0.2789, -0.2517, -0.2234, -0.1918, -0.1649, -0.1432, -0.1392, -0.1256, -0.0969, -0.0708, -0.0463, -0.0212, -0.0067, -0.0006, 0.0063, 0.0246, 0.0318, 0.0426, 0.0469, 0.0459, 0.0347, 0.0127, 0.0093, -0.0036, -0.0127, -0.021, -0.029, -0.036, -0.0384, -0.0337, -0.0458, -0.0566, -0.0707, -0.0833, -0.0947, -0.0978, -0.0959, -0.1047, -0.1038, -0.1099, -0.1109, -0.109, -0.1032, -0.0809, -0.0773, -0.0718, -0.0595, -0.058, -0.0651, -0.0818, -0.0941, -0.1134, -0.1176, -0.1282, -0.1378, -0.1374, -0.1341, -0.1144, -0.1008, -0.0776, -0.056, -0.0335, -0.0156, 0.0032, 0.021, 0.0309, 0.0499, 0.0728, 0.0866, 0.1086, 0.1391, 0.1912, 0.2415, 0.2843, 0.3149, 0.3529, 0.3886, 0.4087, 0.4261, 0.4179, 0.4134, 0.4044, 0.3941, 0.383, 0.3743, 0.3644, 0.3508, 0.3387, 0.3241, 0.306, 0.2919, 0.2651, 0.2491, 0.2138, 0.1721, 0.1304, 0.0971, 0.055, 0.0144, -0.0116, -0.0426, -0.0406, -0.0476, -0.0454, -0.0468, -0.0458, -0.0423]


#长度64











