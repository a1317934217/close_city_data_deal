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

import matplotlib


from networkx.algorithms import approximation as approx
import networkx as nx
import numpy as np
import pandas as pd
from math import e
from math import log
from tqdm import tqdm
import rpy2.robjects as robjects
robjects.r('''
library(igraph)
library('Matrix')
library(purrr)
library(tidyverse)
''')
robjects.r('''
    nodedist<-function(g){
    N<-length(V(g))
    r<-c()
    dg=shortest.paths(g,mode=c("all"),algorithm=c("unweighted"))#geodesic distance
    dg[which(dg==Inf)]=N
    q=setdiff(intersect(dg,dg),0)
    a=Matrix(0,ncol=N,nrow=N)
    for(i in (1:length(q))){
    b=dg
    b[which(b!=q[i])]=0
    a[1:N,q[i]]=colSums(b)/q[i]
}
return(a/(N-1))
}
           ''')
robjects.r('''
            diversity<-function(a){
            div=0
            while(length(a)>1){
            n=sqrt(length(a))
            a[matrix(c(1:n,1:n),ncol=2)]=1
            div=div+min(a)
            escolhas=ceiling(which(a==min(a))/n)
            b=a[escolhas,]
            r<-c()
            for(j in (1:length(escolhas))){
            r<-c(r,sort(b[j,])[2])
            }
            quem=order(r)[1]
            quem=escolhas[quem]
            a=a[setdiff(1:n,quem),setdiff(1:n,quem)]
            n=sqrt(length(a))
            }
            return(div)
            }
           ''')
robjects.r('''
get_diversity_value_list<-function(file_name_path){
        data <-read.csv(file_name_path,fileEncoding = "UTF-8-BOM",skip=1,header = T)
        edges <- data[,1:2]
        graph_test <- graph_from_data_frame(edges, directed = FALSE, vertices=NULL)
        adjacent_distance <- dist(nodedist(graph_test),method="euclidean")
        diversity_value <- diversity(as.matrix(adjacent_distance))
        return(diversity_value)
}
           ''')

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
list_ZJJ = ["常德","长沙","湘西土家族苗族自治州","恩施土家族苗族自治州","益阳","重庆","株洲","岳阳","邵阳","广州","衡阳","深圳"]





# file_path = "F:/封城数据处理/封城数据/石家庄/石家庄四阶/garbage_self_network/deal_01/in/"


#石家庄日期
listXData = getdaylist(20201201, 20210508)


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
def averagenodeconnectivity(file_path,city_name,nodes):
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
    print("平均点连通性： ", listAverageNodeConnectivity)


# 计算城市度
def get_city_degree(file_path,city_name,nodes):
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
    print("城市度： ", list_city_degree)


# 计算边数量
def edge_number(file_path,city_name,nodes):
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
    print("边数量： ", list_edge_number)


# 计算自然连通性
def naturecconnectivity(file_path,city_name,nodes_list):
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
    print("自然连通度： ", listAlgebraicConnectivity)


# 计算密度
def density(file_path,city_name,nodes_list):
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
            # 作为Y轴
            listAlgebraicConnectivity.append(nx.density(G))
    print("密度： ", listAlgebraicConnectivity)



# 计算全球效率
def globalefficiency(file_path,city_name,nodes_list):
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
            # 作为Y轴
            listAlgebraicConnectivity.append(nx.global_efficiency(G))
    print("全球效率： ", listAlgebraicConnectivity)


# 计算diversity
def diversity(file_path,city_name,nodes_list):
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
            t3 = robjects.r['get_diversity_value_list'](robjects.StrVector([filePathInMethon]))
            listAlgebraicConnectivity.append(t3[0])
    print("diversity： ", listAlgebraicConnectivity)




# 计算  点连通性(单个点)
def node_connectivity_alone(file_path,city_name,nodes):
    """
    返回绘制图表的
    X轴：日期
    Y轴：平均点连通性
    """

    listAverageNodeConnectivity = []
    for i in tqdm (range(len(listXData)),desc="点连通性（单个）进度",total=len(listXData)):
        # 循环画图
        try:
            filePathInMethon = file_path + listXData[i] +"_"+city_name+".csv"
            G = drawpicture(filePathInMethon,nodes)

        except Exception as problem:
            print("点连通性（单独） error打开迁徙文件出问题：", problem)
        else:
                listAverageNodeConnectivity.append((nx.node_connectivity(G,s="石家庄",t="唐山")))
    print("点连通性（单独）： ", listAverageNodeConnectivity)




# 计算 平均度
def average_degree_alone(file_path,city_name,nodes):
    listAverage_degree = []
    for i in tqdm(range(len(listXData)), desc="平均度 进度", total=len(listXData)):
        # 循环画图
        try:
            filePathInMethon = file_path + listXData[i] + "_" + city_name + ".csv"
            G = drawpicture(filePathInMethon, nodes)

        except Exception as problem:
            print("平均度   error打开迁徙文件出问题：", problem)
        else:
            d = dict(nx.degree(G))
            listAverage_degree.append(sum(d.values()) / len(G.nodes))

    print("平均度",listAverage_degree)





# 计算 平均最短路径长度
def average_short_length(file_path,city_name,nodes):
    average_short_length_list = []
    global G
    for i in tqdm(range(len(listXData)), desc="平均最短路径长度 进度", total=len(listXData)):
        # 循环画图
        try:
            filePathInMethon = file_path + listXData[i] + "_" + city_name + ".csv"
            print(filePathInMethon)
            G = drawpicture(filePathInMethon, nodes)
        except Exception as problem:
            print("平均最短路径长度   error打开迁徙文件出问题：", problem)
        else:
            S = [G.subgraph(c).copy() for c in nx.connected_components(G)]

            AEC_LastValue = 0
            for C in (G.subgraph(c).copy() for c in nx.connected_components(G)):
                AEC_LastValue = AEC_LastValue + nx.average_shortest_path_length(C)

            average_short_length_list.append(AEC_LastValue / len(S))


    print("平均最短路径长度",average_short_length_list)





# 计算 代数连通性
def algebraic_connectivity(file_path,city_name,nodes):
    algebraic_connectivity_list = []
    for i in tqdm(range(len(listXData)), desc="代数连通性 进度", total=len(listXData)):
        # 循环画图
        try:
            filePathInMethon = file_path + listXData[i] + "_" + city_name + ".csv"
            G = drawpicture(filePathInMethon, nodes)

        except Exception as problem:
            print("代数连通性   error打开迁徙文件出问题：", problem)
        else:

            algebraic_connectivity_list.append(nx.algebraic_connectivity(G))

    print("代数连通性",algebraic_connectivity_list)














if __name__ == '__main__':


    #记得换日期 换日期  换日期 换日期！！！！！！！

    # file_path = "F:/封城数据处理/封城数据/石家庄/石家庄一阶/deal_03/"
    # file_path = "F:/封城数据处理/封城数据/西安/西安一阶/deal_03/"
    # file_path = "F:/封城数据处理/封城数据/张家界/张家界一阶/deal_03/"


    # averagenodeconnectivity(file_path,"张家界",list_ZJJ)
    # get_city_degree(file_path,"张家界",list_ZJJ)
    # edge_number(file_path,"张家界",list_ZJJ)
    # naturecconnectivity(file_path,"张家界",list_ZJJ)


    xingtai_one_network = ["邢台", "北京", "石家庄", "邯郸", "保定", "天津", "衡水", "聊城", "廊坊", "沧州", "济南"]
    beijing_one_network = ["北京", "廊坊", "天津", "保定", "张家口", "唐山", "石家庄", "上海", "承德", "沧州", "邯郸"]
    hengshui_one_network = ["衡水", "石家庄", "北京", "保定", "沧州", "德州", "天津", "张家口", "唐山", "邢台", "廊坊"]
    langfang_one_network = ["廊坊", "北京", "天津", "保定", "沧州", "石家庄", "唐山", "衡水", "张家口", "秦皇岛",
                     "承德"]
    tianjin_one_network = ["天津", "北京", "廊坊", "沧州", "唐山", "保定", "邯郸", "石家庄", "张家口", "秦皇岛", "德州"]



    file_path = "F:/封城数据处理/封城数据/衡水/衡水一阶/deal_03/"
    averagenodeconnectivity(file_path,"衡水",hengshui_one_network)
    get_city_degree(file_path,"衡水",hengshui_one_network)
    edge_number(file_path,"衡水",hengshui_one_network)
    naturecconnectivity(file_path,"衡水",hengshui_one_network)



    # averagenodeconnectivity(file_path, "西安", First_order_xian)
    # get_city_degree(file_path, "西安", First_order_xian)
    # edge_number(file_path, "西安", First_order_xian)
    # naturecconnectivity(file_path, "西安", First_order_xian)



    # density(file_path,"石家庄",First_order_SJZ)
    # diversity(file_path,"石家庄",First_order_SJZ)
    # globalefficiency(file_path,"石家庄",First_order_SJZ)

    # average_short_length(file_path,"西安",First_order_xian)
    # algebraic_connectivity(file_path,"石家庄",First_order_SJZ)


    # node_connectivity_alone(file_path,"石家庄",Five_order_SJZ)
    # average_degree_alone(file_path,"石家庄",Five_order_SJZ)

