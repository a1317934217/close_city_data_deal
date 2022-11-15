# coding:utf-8
"""
@file: visualization_selfnetwork.py
@author: wu hao
@time: 2022/9/28 9:12
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

#石家庄 封城时间 2021/1/7——2021/1/29日  比较时间2021/01/01 -2021/05/08(接近春节) 阈值选取为0.04 确定！
# 石家庄一阶城市 13城市
First_order = ["石家庄","北京","衡水","秦皇岛","唐山","廊坊","天津","承德","保定","沧州","邯郸","邢台","张家口"]
# 石家庄二阶城市 54城市
Second_order =  ['南京', '广州', '长沙', '邯郸', '深圳', '忻州', '长春', '廊坊', '秦皇岛', '锡林郭勒盟', '杭州', '哈尔滨', '三亚', '聊城', '合肥', '沧州', '西安', '衡水', '沈阳', '葫芦岛', '张家口', '苏州', '呼和浩特', '赤峰', '太原', '周口', '天津', '青岛', '潍坊', '菏泽', '济南', '安阳', '北京', '成都', '大同', '滨州', '乌兰察布', '唐山', '临汾', '晋中', '长治', '德州', '浙江', '重庆', '阳泉', '石家庄', '莱芜', '濮阳', '承德', '邢台', '上海', '郑州', '武汉', '保定']
# 石家庄三阶城市 267城市
Third_order =  ['绍兴', '齐齐哈尔', '潍坊', '唐山', '哈尔滨', '大同', '三亚', '天门', '盘锦', '儋州', '平顶山', '湖州', '承德', '南昌', '绥化', '佳木斯', '孝感', '长春', '邵阳', '太原', '玉林', '许昌', '莱芜', '青岛', '晋中', '荆门', '丽水', '泰安', '衡水', '合肥', '长治', '梧州', '烟台', '自贡', '湘潭', '鄂尔多斯', '九江', '辽源', '菏泽', '商丘', '惠州', '连云港', '广西壮族自治区', '三门峡', '汕头', '海口', '天津', '临沂', '浙江', '渭南', '德阳', '常州', '铜仁', '雅安', '乌海', '宜宾', '开封', '揭阳', '苏州', '蚌埠', '邯郸', '伊春', '金华', '宜春', '杭州', '银川', '娄底', '毕节', '随州', '忻州', '黄石', '南通', '枣庄', '萍乡', '辽阳', '朝阳', '吉安', '濮阳', '临汾', '南阳', '株洲', '温州', '毕节地区', '衢州', '南京', '铁岭', '广州', '池州', '西安', '贵港', '鹤岗', '商洛', '韶关', '肇庆', '石家庄', '沧州', '阜阳', '中山', '湛江', '包头', '漯河', '乌兰察布', '阜新', '广元', '东营', '遂宁', '南宁', '巴彦淖尔', '抚顺', '恩施土家族苗族自治州', '郑州', '七台河', '大庆', '廊坊', '六安', '达州', '上饶', '赣州', '日照', '周口', '甘孜藏族自治州', '亳州', '驻马店', '盐城', '松原', '延安', '庆阳', '鹤壁', '嘉兴', '马鞍山', '眉山', '泸州', '芜湖', '镇江', '吕梁', '万宁', '清远', '鞍山', '滁州', '焦作', '益阳', '信阳', '云浮', '长沙', '岳阳', '德州', '运城', '沈阳', '锦州', '淄博', '无锡', '白城', '南充', '舟山', '黄冈', '遵义', '通化', '珠海', '广安', '张家口', '成都', '荆州', '绵阳', '本溪', '郴州', '梅州', '北京', '营口', '贺州', '潜江', '衡阳', '双鸭山', '铜仁地区', '怀化', '平凉', '佛山', '淮南', '咸阳', '阳泉', '内蒙古自治区', '鄂州', '安康', '铜陵', '宿州', '晋城', '巴中', '汉中', '福州', '潮州', '黑河', '仙桃', '常德', '济源', '上海', '茂名', '徐州', '滨州', '攀枝花', '洛阳', '厦门', '延边朝鲜族自治州', '昆明', '黄山', '牡丹江', '吉林', '威海', '呼和浩特', '河源', '湘西土家族苗族自治州', '保定', '东莞', '阳江', '台州', '榆林', '乐山', '内江', '贵阳', '宜昌', '东方', '淮北', '保亭黎族苗族自治县', '凉山彝族自治州', '重庆', '朔州', '兰州', '四平', '宿迁', '葫芦岛', '江门', '陵水黎族自治县', '天水', '资阳', '阿坝藏族羌族自治州', '白山', '丹东', '宝鸡', '济南', '淮安', '泉州', '桂林', '武汉', '琼海', '襄阳', '咸宁', '乐东黎族自治县', '铜川', '锡林郭勒盟', '新乡', '济宁', '邢台', '鸡西', '扬州', '张家界', '秦皇岛', '通辽', '安庆', '深圳', '十堰', '大连', '泰州', '安阳', '赤峰', '宁波', '汕尾', '聊城', '永州', '宣城']
# 石家庄四阶城市 339城市
Fourth_order =  ['扬州', '温州', '池州', '锡林郭勒盟', '南平', '杭州', '黑河', '酒泉', '舟山', '嘉兴', '武汉', '信阳', '攀枝花', '毕节', '威海', '随州', '澳门', '楚雄彝族自治州', '株洲', '琼中黎族苗族自治县', '许昌', '玉溪', '永州', '白城', '蚌埠', '天水', '晋中', '宣城', '昆明', '漳州', '葫芦岛', '益阳', '鹰潭', '青岛', '东方', '桂林', '中卫', '铜陵', '佳木斯', '抚顺', '安康', '襄阳', '遵义', '海东', '玉林', '湘潭', '黔西南布依族苗族自治州', '抚州', '大同', '岳阳', '盘锦', '咸阳', '鹤壁', '淮南', '亳州', '湘西土家族苗族自治州', '张家口', '吴忠', '南昌', '吕梁', '鞍山', '马鞍山', '柳州', '成都', '兴安盟', '齐齐哈尔', '泰安', '濮阳', '邯郸', '锦州', '天门', '泸州', '内蒙古自治区', '长春', '贵港', '南阳', '白山', '湖州', '保定', '六盘水', '上饶', '临高', '郴州', '三明', '来宾', '滁州', '巴中', '阿坝藏族羌族自治州', '绥化', '乌兰察布', '呼和浩特', '绵阳', '宿州', '大庆', '惠州', '廊坊', '万宁', '红河哈尼族彝族自治州', '秦皇岛', '丽水', '梅州', '西双版纳傣族自治州', '韶关', '荆州', '烟台', '百色', '澄迈', '河池', '莆田', '白沙黎族自治县', '深圳', '大连', '汕尾', '萍乡', '双鸭山', '呼伦贝尔', '漯河', '五指山', '宁波', '驻马店', '黄冈', '内江', '北京', '沈阳', '达州', '合肥', '白银', '三门峡', '宜春', '通化', '芜湖', '伊春', '张掖', '松原', '澄迈县', '泉州', '南宁', '宜宾', '周口', '阳泉', '十堰', '济南', '衡水', '安庆', '东营', '济宁', '通辽', '常德', '南充', '七台河', '常州', '宜昌', '东莞', '宿迁', '毕节地区', '临沂', '琼海', '儋州', '鄂州', '怀化', '福州', '定西', '鄂尔多斯', '商丘', '乐东黎族自治县', '乌海', '太原', '海口', '曲靖', '淮安', '陇南', '焦作', '新疆维吾尔自治区', '广元', '衡阳', '鸡西', '黄石', '邢台', '临高县', '珠海', '乐山', '巴彦淖尔', '赣州', '荆门', '无锡', '揭阳', '阿拉善盟', '汕头', '临沧', '吉安', '屯昌县', '仙桃', '佛山', '丹东', '九江', '金昌', '云浮', '晋城', '石家庄', '洛阳', '银川', '张家界', '定安', '安阳', '临汾', '南通', '保亭黎族苗族自治县', '淄博', '文山壮族苗族自治州', '新余', '营口', '渭南', '平顶山', '临夏回族自治州', '陵水黎族自治县', '中山', '固原', '西安', '连云港', '徐州', '江门', '聊城', '资阳', '德州', '武威', '淮北', '上海', '遂宁', '阳江', '南京', '自贡', '钦州', '贺州', '济源', '辽阳', '海东地区', '浙江', '潮州', '西宁', '景德镇', '菏泽', '龙岩', '运城', '梧州', '朔州', '郑州', '包头', '四平', '恩施土家族苗族自治州', '三亚', '贵阳', '黔南布依族苗族自治州', '哈尔滨', '安顺', '黔东南苗族侗族自治州', '吉林', '崇左', '河源', '日照', '牡丹江', '延边朝鲜族自治州', '辽源', '眉山', '宝鸡', '苏州', '潍坊', '潜江', '朝阳', '石嘴山', '广州', '娄底', '莱芜', '长治', '邵阳', '承德', '昌江黎族自治县', '枣庄', '西藏自治区', '文昌', '大理白族自治州', '铜仁', '茂名', '凉山彝族自治州', '甘南藏族自治州', '铁岭', '德宏傣族景颇族自治州', '昭通', '阜阳', '阜新', '黄山', '湛江', '广安', '盐城', '延安', '保山', '本溪', '普洱', '庆阳', '孝感', '鹤岗', '肇庆', '甘孜藏族自治州', '台州', '泰州', '定安县', '沧州', '赤峰', '绍兴', '开封', '铜仁地区', '金华', '天津', '商洛', '滨州', '汉中', '兰州', '平凉', '防城港', '广西壮族自治区', '厦门', '宁夏回族自治区', '宁德', '铜川', '唐山', '长沙', '六安', '北海', '镇江', '忻州', '重庆', '衢州', '屯昌', '清远', '雅安', '榆林', '咸宁', '新乡', '丽江', '德阳']
#石家庄五阶 336城市
Five_order = ['烟台', '文山壮族苗族自治州', '仙桃', '铜川', '泰州', '扬州', '聊城', '鹰潭', '抚顺', '汉中', '无锡', '莱芜', '泰安', '芜湖', '梧州', '钦州', '万宁', '长沙', '平凉', '延安', '常德', '德阳', '常州', '永州', '枣庄', '阿拉善盟', '安康', '沈阳', '文昌', '曲靖', '赣州', '荆州', '甘南藏族自治州', '朝阳', '河源', '保亭黎族苗族自治县', '苏州', '定安', '黄冈', '绥化', '白沙黎族自治县', '青岛', '潮州', '琼海', '衢州', '黔西南布依族苗族自治州', '天津', '马鞍山', '海西蒙古族藏族自治州', '吉安', '亳州', '兴安盟', '朔州', '长治', '南充', '潍坊', '濮阳', '娄底', '玉林', '宿迁', '凉山彝族自治州', '湘潭', '淮安', '包头', '屯昌县', '杭州', '咸宁', '大同', '葫芦岛', '盘锦', '重庆', '雅安', '绵阳', '临高县', '孝感', '渭南', '海东地区', '九江', '益阳', '鹤壁', '张家口', '舟山', '忻州', '龙岩', '白城', '许昌', '佳木斯', '楚雄彝族自治州', '平顶山', '铜陵', '商丘', '大理白族自治州', '西宁', '内江', '新余', '自贡', '海口', '武汉', '资阳', '辽源', '丹东', '三亚', '张家界', '乌海', '海南藏族自治州', '珠海', '攀枝花', '佛山', '莆田', '安顺', '乐山', '六盘水', '廊坊', '儋州', '南平', '临沧', '鹤岗', '承德', '衡阳', '黄山', '随州', '北海', '揭阳', '汕头', '大连', '临汾', '晋中', '阳泉', '黔东南苗族侗族自治州', '衡水', '中山', '桂林', '温州', '琼中黎族苗族自治县', '铜仁', '榆林', '延边朝鲜族自治州', '白银', '商洛', '遵义', '滁州', '潜江', '定西', '淄博', '锦州', '怀化', '丽水', '福州', '哈密地区', '乌兰察布', '中卫', '邵阳', '南昌', '贺州', '三明', '滨州', '大庆', '黄南藏族自治州', '金昌', '济源', '兰州', '甘孜藏族自治州', '六安', '玉溪', '哈尔滨', '通化', '吴忠', '上海', '宿州', '营口', '漯河', '邯郸', '株洲', '唐山', '嘉兴', '辽阳', '天门', '漳州', '阳江', '邢台', '淮南', '宜宾', '屯昌', '鄂尔多斯', '菏泽', '绍兴', '松原', '河池', '日照', '湖州', '北京', '咸阳', '南通', '宜春', '广州', '济南', '哈密', '汕尾', '铁岭', '通辽', '临沂', '长春', '银川', '陇南', '泉州', '运城', '防城港', '鄂州', '惠州', '保定', '石嘴山', '焦作', '洛阳', '迪庆藏族自治州', '广元', '岳阳', '广安', '晋城', '昭通', '铜仁地区', '湛江', '西安', '台州', '固原', '韶关', '巴彦淖尔', '眉山', '红河哈尼族彝族自治州', '达州', '新乡', '赤峰', '恩施土家族苗族自治州', '百色', '昆明', '郑州', '合肥', '阜阳', '盐城', '太原', '白山', '泸州', '十堰', '武威', '石家庄', '崇左', '秦皇岛', '吉林', '嘉峪关', '海东', '荆门', '锡林郭勒盟', '安庆', '湘西土家族苗族自治州', '宁德', '柳州', '庆阳', '丽江', '信阳', '郴州', '临高', '阿坝藏族羌族自治州', '云浮', '贵阳', '德州', '镇江', '周口', '蚌埠', '本溪', '梅州', '昌都', '成都', '深圳', '遂宁', '定安县', '酒泉', '连云港', '徐州', '济宁', '昌都地区', '陵水黎族自治县', '海北藏族自治州', '金华', '南京', '宣城', '池州', '茂名', '双鸭山', '抚州', '四平', '开封', '乐东黎族自治县', '威海', '齐齐哈尔', '东莞', '宜昌', '澳门', '临夏回族自治州', '三门峡', '江门', '黄石', '景德镇', '普洱', '西双版纳傣族自治州', '澄迈县', '襄阳', '毕节地区', '毕节', '南宁', '宝鸡', '东营', '来宾', '淮北', '巴中', '澄迈', '黔南布依族苗族自治州', '东方', '怒江傈僳族自治州', '厦门', '贵港', '清远', '萍乡', '鞍山', '保山', '肇庆', '天水', '呼和浩特', '吕梁', '阜新', '驻马店', '安阳', '昌江黎族自治县', '上饶', '沧州', '张掖', '宁波', '南阳']
#石家庄六阶 城市直接全部包括




#西安 封城时间 20211223 20220115  比较时间2021/12/09 -2022/1/31(接近春节) 阈值选取为0.08 确定！
#16个
First_order_xian =  ['北京', '郑州', '成都', '宝鸡', '榆林', '铜川', '汉中', '延安', '咸阳', '商洛', '庆阳', '兰州', '安康', '运城', '渭南', '西安']
#89个
Second_order_xian =  ['临汾', '兰州', '廊坊', '呼和浩特', '汉中', '延安', '铜川', '西安', '宜宾', '周口', '上海', '榆林', '遂宁', '成都', '石家庄', '广元', '凉山彝族自治州', '达州', '白银', '邯郸', '庆阳', '攀枝花', '邢台', '济南', '衡水', '张家口', '新乡', '洛阳', '贵阳', '沈阳', '焦作', '广安', '阿坝藏族羌族自治州', '沧州', '莱芜', '雅安', '开封', '甘南藏族自治州', '保定', '自贡', '眉山', '青岛', '商丘', '濮阳', '甘孜藏族自治州', '天津', '乐山', '武汉', '南阳', '南京', '安阳', '资阳', '三门峡', '南充', '巴中', '信阳', '临夏回族自治州', '吕梁', '咸阳', '昆明', '秦皇岛', '绵阳', '定西', '驻马店', '漯河', '商洛', '泸州', '运城', '宝鸡', '平顶山', '许昌', '重庆', '鹤壁', '唐山', '郑州', '北京', '天水', '太原', '渭南', '承德', '安康', '深圳', '德阳', '武威', '鄂尔多斯', '忻州', '银川', '西宁', '内江']

#225个
Third_order_xian =  ['惠州', '黔西南布依族苗族自治州', '中卫', '鄂尔多斯', '商洛', '东莞', '珠海', '梅州', '汕尾', '贵阳', '洛阳', '威海', '葫芦岛', '孝感', '扬州', '鄂州', '湖州', '商丘', '廊坊', '杭州', '长沙', '遂宁', '许昌', '潍坊', '宣城', '昭通', '张家口', '甘南藏族自治州', '常州', '连云港', '泸州', '阳泉', '仙桃', '枣庄', '南充', '衡水', '安顺', '鞍山', '阿坝藏族羌族自治州', '海北藏族自治州', '忻州', '天门', '淄博', '遵义', '东营', '毕节地区', '陇南', '自贡', '固原', '泰州', '亳州', '南京', '北京', '咸宁', '定西', '巴彦淖尔', '金华', '漯河', '昆明', '沧州', '邯郸', '宝鸡', '长治', '沈阳', '临沂', '咸阳', '广安', '信阳', '德阳', '铜仁地区', '大同', '榆林', '眉山', '宜宾', '日照', '聊城', '乐山', '丽江', '肇庆', '烟台', '宿迁', '临汾', '锦州', '呼和浩特', '凉山彝族自治州', '保山', '安康', '盐城', '铜仁', '达州', '佛山', '石家庄', '恩施土家族苗族自治州', '莱芜', '普洱', '朝阳', '海南藏族自治州', '重庆', '大连', '红河哈尼族彝族自治州', '金昌', '甘孜藏族自治州', '文山壮族苗族自治州', '鹤壁', '营口', '天水', '平顶山', '唐山', '宿州', '舟山', '铁岭', '汕头', '滨州', '淮安', '德州', '吕梁', '芜湖', '海西蒙古族藏族自治州', '楚雄彝族自治州', '临夏回族自治州', '黔东南苗族侗族自治州', '乌兰察布', '毕节', '阜新', '温州', '广元', '潜江', '成都', '青岛', '黄南藏族自治州', '运城', '三门峡', '黄冈', '随州', '江门', '石嘴山', '武汉', '盘锦', '保定', '本溪', '西双版纳傣族自治州', '无锡', '丹东', '清远', '雅安', '乌海', '渭南', '合肥', '绵阳', '深圳', '朔州', '驻马店', '海东地区', '武威', '西安', '庆阳', '绍兴', '滁州', '辽阳', '银川', '抚顺', '十堰', '韶关', '黄石', '晋城', '汉中', '镇江', '吴忠', '宁波', '济源', '秦皇岛', '兰州', '安阳', '马鞍山', '周口', '海东', '上海', '包头', '白银', '郑州', '西宁', '六盘水', '晋中', '襄阳', '济宁', '承德', '六安', '荆门', '巴中', '赣州', '泰安', '太原', '菏泽', '大理白族自治州', '开封', '濮阳', '揭阳', '湛江', '黔南布依族苗族自治州', '徐州', '阜阳', '攀枝花', '广州', '南阳', '茂名', '河源', '铜川', '焦作', '玉溪', '延安', '济南', '天津', '资阳', '宜昌', '南通', '曲靖', '长春', '内江', '临沧', '荆州', '新乡', '邢台', '中山', '苏州', '嘉兴']

#277个
Fourth_order_xian =  ['衡水', '太原', '榆林', '怀化', '徐州', '上饶', '滨州', '菏泽', '镇江', '资阳', '延安', '绵阳', '湛江', '宜春', '黔南布依族苗族自治州', '安顺', '昆明', '安康', '湘西土家族苗族自治州', '辽源', '莱芜', '阳江', '吕梁', '甘孜藏族自治州', '黔东南苗族侗族自治州', '临沧', '湘潭', '许昌', '大理白族自治州', '聊城', '抚顺', '烟台', '池州', '延边朝鲜族自治州', '廊坊', '鞍山', '昭通', '定西', '保山', '铜仁地区', '宿迁', '安阳', '扬州', '黔西南布依族苗族自治州', '兰州', '宿州', '朔州', '沈阳', '海南藏族自治州', '乌海', '海北藏族自治州', '凉山彝族自治州', '舟山', '商洛', '滁州', '淮北', '普洱', '三门峡', '襄阳', '北京', '东营', '广元', '南昌', '咸宁', '临沂', '楚雄彝族自治州', '长治', '西双版纳傣族自治州', '济南', '上海', '德阳', '江门', '文山壮族苗族自治州', '苏州', '阿坝藏族羌族自治州', '肇庆', '青岛', '岳阳', '日照', '沧州', '四平', '信阳', '深圳', '百色', '银川', '株洲', '大同', '玉林', '潮州', '驻马店', '眉山', '武汉', '德州', '达州', '赤峰', '甘南藏族自治州', '通化', '遂宁', '武威', '济源', '吴忠', '芜湖', '海西蒙古族藏族自治州', '商丘', '荆门', '白山', '石嘴山', '常德', '宁波', '台州', '益阳', '淮南', '泰州', '宝鸡', '南通', '金昌', '六安', '本溪', '铜仁', '怒江傈僳族自治州', '曲靖', '广州', '忻州', '揭阳', '辽阳', '雅安', '毕节', '咸阳', '佛山', '济宁', '焦作', '乐山', '马鞍山', '郑州', '湖州', '鄂州', '宣城', '张家口', '杭州', '荆州', '广安', '永州', '邵阳', '惠州', '晋城', '海口', '丽水', '娄底', '庆阳', '秦皇岛', '石家庄', '梅州', '九江', '随州', '晋中', '白银', '宜昌', '温州', '阜阳', '平顶山', '宜宾', '攀枝花', '连云港', '铁岭', '黄冈', '重庆', '绍兴', '嘉兴', '淮安', '十堰', '松原', '威海', '澳门', '黄南藏族自治州', '恩施土家族苗族自治州', '蚌埠', '丽江', '长春', '乌兰察布', '六盘水', '锦州', '开封', '呼和浩特', '泸州', '阿拉善盟', '营口', '铜川', '铜陵', '吉安', '黄山', '南宁', '潍坊', '南京', '包头', '河源', '东莞', '张家界', '漯河', '阜新', '梧州', '盘锦', '无锡', '天津', '陇南', '衡阳', '汕尾', '常州', '郴州', '合肥', '金华', '自贡', '邢台', '遵义', '周口', '保定', '内江', '大连', '吉林', '洛阳', '安庆', '唐山', '枣庄', '阳泉', '潜江', '西安', '成都', '中卫', '贵港', '临汾', '渭南', '鹤壁', '汕头', '运城', '宁德', '南阳', '南充', '白城', '汉中', '亳州', '泰安', '中山', '盐城', '巴中', '西宁', '朝阳', '海东', '固原', '巴彦淖尔', '玉溪', '承德', '天门', '鄂尔多斯', '贵阳', '濮阳', '茂名', '萍乡', '红河哈尼族彝族自治州', '珠海', '毕节地区', '仙桃', '黄石', '衢州', '葫芦岛', '淄博', '临夏回族自治州', '赣州', '韶关', '清远', '邯郸', '云浮', '孝感', '天水', '迪庆藏族自治州', '新乡', '丹东', '海东地区', '长沙']
#309个
five_order_xian = ['资阳', '楚雄彝族自治州', '天水', '鞍山', '固原', '铜川', '柳州', '日照', '福州', '中山', '孝感', '眉山', '西宁', '铜陵', '揭阳', '海南藏族自治州', '无锡', '南阳', '白银', '云浮', '盘锦', '温州', '肇庆', '随州', '岳阳', '甘南藏族自治州', '舟山', '深圳', '松原', '张家口', '驻马店', '西安', '南昌', '百色', '盐城', '自贡', '雅安', '玉溪', '洛阳', '鄂州', '来宾', '连云港', '屯昌', '石家庄', '河池', '巴彦淖尔', '上海', '黄冈', '咸阳', '莱芜', '丽水', '济宁', '仙桃', '内江', '烟台', '南通', '临沧', '威海', '朔州', '渭南', '恩施土家族苗族自治州', '贵阳', '淮北', '丽江', '吕梁', '天门', '白城', '朝阳', '定西', '茂名', '汉中', '沧州', '聊城', '万宁', '锦州', '儋州', '黄石', '白山', '阜阳', '绍兴', '安顺', '宝鸡', '湛江', '毕节地区', '大同', '蚌埠', '昭通', '扬州', '湘西土家族苗族自治州', '常德', '泸州', '景德镇', '乌海', '屯昌县', '株洲', '阳泉', '六安', '榆林', '沈阳', '文山壮族苗族自治州', '中卫', '汕尾', '台州', '凉山彝族自治州', '滨州', '安康', '阿拉善盟', '西双版纳傣族自治州', '黔南布依族苗族自治州', '晋中', '昆明', '临高', '大连', '潍坊', '红河哈尼族彝族自治州', '黔东南苗族侗族自治州', '襄阳', '延边朝鲜族自治州', '湖州', '江门', '周口', '遂宁', '德州', '甘孜藏族自治州', '呼和浩特', '延安', '大理白族自治州', '赤峰', '定安', '重庆', '阜新', '枣庄', '永州', '阿坝藏族羌族自治州', '嘉兴', '营口', '河源', '泰安', '六盘水', '韶关', '新余', '海北藏族自治州', '庆阳', '临汾', '咸宁', '铜仁地区', '镇江', '金昌', '郑州', '三门峡', '邯郸', '邵阳', '兴安盟', '长治', '临高县', '苏州', '北海', '包头', '淮南', '南宁', '桂林', '北京', '廊坊', '安庆', '佛山', '海西蒙古族藏族自治州', '钦州', '长春', '锡林郭勒盟', '迪庆藏族自治州', '合肥', '本溪', '安阳', '衡阳', '萍乡', '贺州', '娄底', '梧州', '忻州', '新乡', '唐山', '商丘', '亳州', '抚州', '辽源', '宜春', '平顶山', '马鞍山', '益阳', '南京', '辽阳', '陵水黎族自治县', '保定', '成都', '晋城', '德阳', '石嘴山', '琼海', '青岛', '武威', '张家界', '潮州', '焦作', '澄迈', '东莞', '兰州', '普洱', '达州', '潜江', '铁岭', '太原', '漯河', '玉林', '宜昌', '文昌', '鹤壁', '临沂', '宜宾', '信阳', '攀枝花', '广元', '乐山', '鹰潭', '崇左', '濮阳', '汕头', '承德', '葫芦岛', '宣城', '运城', '防城港', '杭州', '宁波', '珠海', '商洛', '惠州', '菏泽', '泰州', '郴州', '曲靖', '衡水', '广州', '济南', '衢州', '广安', '上饶', '十堰', '临夏回族自治州', '宿州', '怒江傈僳族自治州', '东营', '滁州', '吉安', '通辽', '常州', '清远', '银川', '济源', '贵港', '东方', '荆州', '邢台', '抚顺', '淄博', '九江', '丹东', '绵阳', '巴中', '陇南', '黄山', '毕节', '宿迁', '乌兰察布', '三亚', '芜湖', '保山', '武汉', '徐州', '荆门', '秦皇岛', '吉林', '赣州', '澄迈县', '梅州', '许昌', '澳门', '黔西南布依族苗族自治州', '四平', '池州', '海东', '鄂尔多斯', '开封', '南充', '黄南藏族自治州', '阳江', '通化', '金华', '长沙', '遵义', '铜仁', '海东地区', '吴忠', '宁德', '怀化', '海口', '湘潭', '淮安', '天津', '定安县']
#西安六阶全部相同

# 根据路径画图
def drawpicture(filePath,nodes_list_add):
    """
    输入文件路径最后绘制成图G
    """
    global dataMiga
    G = nx.Graph()
    G.add_nodes_from(nodes_list_add)
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
#西安 封城时间 20211223 20220115  比较时间2021/12/09 -2022/1/31(接近春节) 阈值选取为0.08 确定！



#石家庄 封城时间 2021/1/7——2021/1/29日  比较时间2021/01/01 -2021/05/08(接近春节) 阈值选取为0.04 确定！
#石家庄封城前(20210101)   石家庄封城时(20210114)    石家庄封城后(20210301)

# G_one = drawpicture("F:/封城数据处理/封城数据/石家庄/石家庄一阶/deal_03/20210101_石家庄.csv",First_order)
#
#
# G_two = drawpicture("F:/封城数据处理/封城数据/石家庄/石家庄一阶/deal_03/20210114_石家庄.csv",First_order)
# G_three = drawpicture("F:/封城数据处理/封城数据/石家庄/石家庄一阶/deal_03/20210223_石家庄.csv",First_order)
# G_four = drawpicture("F:/封城数据处理/封城数据/西安/西安四阶/deal_03/20220130_西安.csv",Fourth_order_xian)
# G_five = drawpicture("F:/封城数据处理/封城数据/西安/西安五阶/deal_03/20220130_西安.csv",five_order_xian)


G_one = drawpicture("F:/封城数据处理/封城数据/石家庄/石家庄一阶/deal_03/20210301_石家庄.csv",First_order)
G_two = drawpicture("F:/封城数据处理/封城数据/石家庄/石家庄二阶/deal_03/20210301_石家庄.csv",Second_order)
G_three = drawpicture("F:/封城数据处理/封城数据/石家庄/石家庄三阶/deal_03/20210301_石家庄.csv",Third_order)
G_four = drawpicture("F:/封城数据处理/封城数据/石家庄/石家庄四阶/deal_03/20210301_石家庄.csv",Fourth_order)
G_five = drawpicture("F:/封城数据处理/封城数据/石家庄/石家庄五阶/deal_03/20210301_石家庄.csv",Five_order)


plt.figure(figsize=(7,5),dpi=450)
plt.rcParams['font.sans-serif'] = ['SimHei']



pos_one = nx.circular_layout(G_one)
pos_one["石家庄"] = (0,0)
plt.subplot(231)
plt.title("(a) 一阶")
nx.draw(G_one, pos_one,font_size=12,with_labels = True,node_color = "red",node_size = 12)




pos_two = nx.kamada_kawai_layout(G_two)
labels = {}
# labels["石家庄"] = "石家庄"
plt.subplot(232)
plt.title("(b) 二阶")
print()
nx.draw(G_two, pos_two,node_color = "red",node_size = 6)
nx.draw_networkx_labels(G_two,pos_two,labels,font_size=12,font_color='b')


plt.subplot(233)
pos_three = nx.kamada_kawai_layout(G_three)
pos_three["石家庄"] = (0,0)
plt.title("(c) 三阶")
nx.draw(G_three, pos_three,node_color = "red",node_size = 6)
nx.draw_networkx_labels(G_three,pos_three,labels,font_size=12,font_color='w')
#
#
plt.subplot(234)

pos_four = nx.kamada_kawai_layout(G_four)
pos_four["石家庄"] = (0,0)
plt.title("(d) 四阶")
nx.draw(G_four, pos_four,node_color = "red",node_size = 6)
nx.draw_networkx_labels(G_four,pos_four,labels,font_size=12,font_color='w')



plt.subplot(235)
pos_five = nx.kamada_kawai_layout(G_five)
pos_five["石家庄"] = (0,0)
plt.title("(e) 五阶")
nx.draw(G_five, pos_five,node_color = "red",node_size = 6)
nx.draw_networkx_labels(G_five,pos_five,labels,font_size=12,font_color='w')






plt.show()
