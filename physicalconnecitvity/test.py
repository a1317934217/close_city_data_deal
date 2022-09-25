#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 9:32
# @Author  : wuhao
# @Email   : guess?????
# @File    : deledatainfo.py
import datetime
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
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

# 根据路径画图
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
# 需要留下的节点
lastname = {'威海', '三门峡', '白沙黎族自治县', '攀枝花', '陵水黎族自治县', '通辽', '桂林', '汕头', '枣庄', '绵阳', '达州', '阜阳', '普洱', '榆林', '齐齐哈尔', '衢州', '邢台', '嘉峪关', '益阳', '商丘', '天水', '恩施土家族苗族自治州', '云浮', '哈密', '德宏傣族景颇族自治州', '昌江黎族自治县', '白城', '秦皇岛', '铁岭', '四平', '咸阳', '平凉', '佳木斯', '万宁', '广州', '陇南', '临夏回族自治州', '昭通', '南通', '本溪', '开封', '青岛', '玉溪', '三亚', '哈尔滨', '三明', '阜新', '衡水', '西宁', '淮南', '来宾', '东莞', '保定', '承德', '马鞍山', '安康', '佛山', '白山', '百色', '丽水', '延边朝鲜族自治州', '沧州', '东营', '邵阳', '遵义', '赣州', '驻马店', '凉山彝族自治州', '中山', '菏泽', '襄樊', '泰州', '北海', '崇左', '兰州', '芜湖', '思茅', '白银', '临高县', '中卫', '文山壮族苗族自治州', '绥化', '焦作', '钦州', '六盘水', '荆门', '张掖', '楚雄彝族自治州', '大理白族自治州', '大庆', '吴忠', '柳州', '池州', '福州', '常州', '玉林', '黔东南苗族侗族自治州', '澳门', '东方', '安阳', '抚顺', '黄冈', '南充', '苏州', '黄石', '香港', '泰安', '长春', '景德镇', '龙岩', '阳江', '湘潭', '河池', '庆阳', '宜春', '张家口', '贺州', '揭阳', '潍坊', '黄南藏族自治州', '拉萨', '铜川', '宣城', '平顶山', '德州', '常德', '锡林郭勒盟', '防城港', '昆明', '琼海', '兴安盟', '渭南', '文昌', '阳泉', '鹤壁', '襄阳', '和田地区', '淮安', '咸宁', '南宁', '海东', '乌海', '广安', '呼和浩特', '安顺', '遂宁', '蚌埠', '黑河', '潜江', '天门', '重庆', '大同', '镇江', '武汉', '黄山', '鹤岗', '江门', '营口', '海口', '岳阳', '澄迈县', '巴音郭楞蒙古自治州', '廊坊', '临沂', '乌兰察布', '无锡', '吕梁', '黔南布依族苗族自治州', '定西', '怀化', '株洲', '九江', '南昌', '延安', '阿拉善盟', '贵港', '绍兴', '忻州', '商洛', '长治', '韶关', '宿州', '烟台', '巴中', '梧州', '松原', '太原', '随州', '南平', '乌鲁木齐', '郑州', '喀什地区', '博尔塔拉蒙古自治州', '聊城', '唐山', '酒泉', '海西蒙古族藏族自治州', '丹东', '朝阳', '昆玉', '濮阳', '神农架林区', '儋州', '衡阳', '果洛藏族自治州', '滁州', '辽源', '曲靖', '贵阳', '抚州', '琼中黎族苗族自治县', '萍乡', '银川', '牡丹江', '周口', '成都', '金昌', '湖州', '宿迁', '鹰潭', '朔州', '徐州', '六安', '乐东黎族自治县', '许昌', '包头', '通化', '漯河', '南阳', '肇庆', '迪庆藏族自治州', '清远', '吉林', '赤峰', '孝感', '武威', '吉安', '毕节', '新乡', '晋城', '日照', '长沙', '仙桃', '淮北', '鄂尔多斯', '淄博', '荆州', '汕尾', '安庆', '杭州', '德阳', '大兴安岭地区', '宜昌', '眉山', '阿坝藏族羌族自治州', '厦门', '合肥', '沈阳', '伊犁哈萨克自治州', '娄底', '巴彦淖尔', '温州', '上海', '西安', '雅安', '天津', '图木舒克', '阿克苏地区', '运城', '连云港', '潮州', '金华', '乐山', '晋中', '永州', '济南', '扬州', '锦州', '宝鸡', '临汾', '宁德', '河源', '北京', '珠海', '漳州', '深圳', '南京', '亳州', '大连', '湘西土家族苗族自治州', '甘孜藏族自治州', '鞍山', '呼伦贝尔', '信阳', '红河哈尼族彝族自治州', '汉中', '石嘴山', '惠州', '滨州', '七台河', '梅州', '洛阳', '辽阳', '丽江', '十堰', '湛江', '泉州', '石家庄', '黔西南布依族苗族自治州', '宁波', '盐城', '玉树藏族自治州', '嘉兴', '台州', '泸州', '铜仁', '茂名', '伊春', '定安县', '葫芦岛', '资阳', '济源', '邯郸', '甘南藏族自治州', '广元', '上饶', '郴州', '盘锦', '济宁'}
# 需要删除的节点
delNeedNode =['定安', '屯昌', '澄迈', '临高', '海东地区', '昌都地区', '山南地区', '日喀则地区', '那曲地区', '林芝地区', '吐鲁番地区', '铜仁地区', '毕节地区', '广西壮族自治区', '内蒙古自治区', '宁夏回族自治区', '新疆维吾尔自治区', '西藏自治区', '吉林市', '鸡西', '双鸭山', '浙江', '舟山', '铜陵', '莆田', '新余', '莱芜', '鄂州', '张家界', '五指山', '自贡', '内江', '宜宾', '保山', '临沧', '固原', '克拉玛依', '石河子', '阿拉尔', '五家渠', '北屯', '铁门关', '双河', '可克达拉', '保亭黎族苗族自治县', '西双版纳傣族自治州', '怒江傈僳族自治州', '阿里地区', '海北藏族自治州', '海南藏族自治州', '昌吉回族自治州', '哈密地区', '克孜勒苏柯尔克孜自治州', '塔城地区', '阿勒泰地区']
dayList = getdaylist(20200101,20211028)

try:
    filePathName = "F:\\01大连民族\\百度迁徙爬取和数据\\百度迁徙数据-final\\物理联通指标所需数据\\resultdata\\20200101physical.csv"
    dataWantdelCol = pd.read_csv(filePathName)
except Exception as problem:
    print("error打开physical本地数据有问题：", problem)
else:
    counntnum = len(dataWantdelCol)
    G = nx.Graph()
    for i in range(counntnum):
        indexColDel = dataWantdelCol.loc[i]
        if float(indexColDel[2]) < 0.04:
            # 获取到索引
            # indexDel = dataWantdelCol[(dataWantdelCol.city_name == indexColDel[0]) & (dataWantdelCol.city_id_name == indexColDel[1])].index.tolist()[0]
            dataWantdelCol.drop(i, axis=0, inplace=True)
            # print("移除数据",indexColMoveOut)
    dataWantdelCol = dataWantdelCol.reset_index(drop=True)
    print(dataWantdelCol)
    # 去掉小于0.04的边
    for row in dataWantdelCol.itertuples():
        city_name = getattr(row, "city_name")
        city_id_name = getattr(row, "city_id_name")
        G.add_edges_from([(city_name, city_id_name)])
    #去掉不需要的点
    G.remove_nodes_from(delNeedNode)

    pos = nx.spring_layout(G)
    nx.draw(G, pos)
    mode_labels = nx.get_node_attributes(G, 'desc')
    nx.draw_networkx_nodes(G, pos, label=mode_labels)
    plt.show()
    print(G)

