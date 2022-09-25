#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/13 18:00
# @Author  : wuhao
# @Email   : guess?????
# @File    : diversityvalue.py
import collections
import csv

import networkx as nx
import pandas as pd
import rpy2.robjects as robjects

#‘pi’为R的内置变量
# 第一种
# t0 = robjects.r['pi']
# print(t0[0])

# creat an R function，自定义R函数
#python 调用RRRR
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
        G.add_edges_from([(city_name, city_id_name)])
    return G

listXData = ['20200101', '20200102', '20200103', '20200104', '20200105', '20200106', '20200107', '20200108', '20200109', '20200110', '20200111', '20200112', '20200113', '20200114', '20200115', '20200116', '20200117', '20200118', '20200119', '20200120', '20200121', '20200122', '20200123', '20200124', '20200125', '20200126', '20200127', '20200128', '20200129', '20200130', '20200131', '20200201', '20200202', '20200203', '20200204', '20200205', '20200206', '20200207', '20200208', '20200209', '20200210', '20200211', '20200212', '20200213', '20200214', '20200215', '20200216', '20200217', '20200218', '20200219', '20200220', '20200221', '20200222', '20200223', '20200224', '20200225', '20200226', '20200227', '20200228', '20200229', '20200301', '20200302', '20200303', '20200304', '20200305', '20200306', '20200307', '20200308', '20200309', '20200310', '20200311', '20200312', '20200313', '20200314', '20200315', '20200316', '20200317', '20200318', '20200319', '20200320', '20200321', '20200322', '20200323', '20200324', '20200325', '20200326', '20200327', '20200328', '20200329', '20200330', '20200331', '20200401', '20200402', '20200403', '20200404', '20200405', '20200406', '20200407', '20200408', '20200409', '20200410', '20200411', '20200412', '20200413', '20200414', '20200415', '20200416', '20200417', '20200418', '20200419', '20200420', '20200421', '20200422', '20200423', '20200424', '20200425', '20200426', '20200427', '20200428', '20200429', '20200430', '20200501', '20200502', '20200503']
nodeList=['舟山', '贵阳', '黄石', '昭通', '焦作', '南通', '丽水', '晋城', '巴中', '阜新', '合肥', '威海', '宿州', '德阳', '白山', '延安', '攀枝花', '佛山', '亳州', '天门', '濮阳', '池州', '漯河', '盐城', '厦门', '丹东', '保山', '贵港', '南昌', '绵阳', '黄冈', '廊坊', '鄂州', '渭南', '宣城', '乐山', '昆明', '淮安', '云浮', '南京', '长治', '防城港', '鞍山', '泸州', '大连', '阳泉', '盘锦', '温州', '赣州', '荆门', '西宁', '湘西土家族苗族自治州', '吉安', '开封', '铜陵', '孝感', '呼和浩特', '佳木斯', '枣庄', '眉山', '遂宁', '武汉', '许昌', '达州', '青岛', '承德', '咸阳', '驻马店', '天水', '苏州', '长春', '黑河', '连云港', '红河哈尼族彝族自治州', '辽阳', '六安', '菏泽', '衡水', '营口', '兴安盟', '岳阳', '黔南布依族苗族自治州', '湘潭', '泉州', '齐齐哈尔', '平顶山', '武威', '宜昌', '滁州', '江门', '临沧', '玉溪', '郴州', '葫芦岛', '沈阳', '商丘', '潜江', '南充', '嘉兴', '东莞', '广安', '恩施土家族苗族自治州', '乌兰察布', '潍坊', '襄阳', '天津', '茂名', '大庆', '邢台', '镇江', '张掖', '河源', '东营', '绥化', '马鞍山', '台州', '抚顺', '柳州', '西双版纳傣族自治州', '西安', '白银', '蚌埠', '揭阳', '宜春', '九江', '邵阳', '阜阳', '四平', '张家口', '湛江', '铁岭', '德宏傣族景颇族自治州', '普洱', '荆州', '伊春', '济宁', '烟台', '珠海', '太原', '本溪', '惠州', '无锡', '双鸭山', '安阳', '运城', '衡阳', '广州', '玉林', '淮北', '凉山彝族自治州', '自贡', '常德', '海南藏族自治州', '长沙', '宁德', '呼伦贝尔', '百色', '新乡', '包头', '甘孜藏族自治州', '朔州', '辽源', '海西蒙古族藏族自治州', '张家界', '重庆', '庆阳', '聊城', '泰州', '上饶', '曲靖', '郑州', '中山', '安顺', '白城', '漳州', '淮南', '桂林', '南宁', '益阳', '济源', '文山壮族苗族自治州', '北海', '抚州', '阳江', '秦皇岛', '梅州', '成都', '德州', '锦州', '安康', '巴彦淖尔', '河池', '汕头', '通化', '龙岩', '梧州', '宜宾', '莆田', '济南', '安庆', '萍乡', '深圳', '日照', '赤峰', '宁波', '平凉', '邯郸', '丽江', '大同', '汕尾', '株洲', '宿迁', '怀化', '钦州', '哈尔滨', '南平', '宝鸡', '鹤岗', '榆林', '通辽', '随州', '泰安', '鹤壁', '朝阳', '资阳', '雅安', '仙桃', '信阳', '楚雄彝族自治州', '潮州', '绍兴', '周口', '常州', '吕梁', '忻州', '景德镇', '三明', '鹰潭', '杭州', '金华', '鄂尔多斯', '衢州', '牡丹江', '陇南', '铜川', '扬州', '临夏回族自治州', '阿坝藏族羌族自治州', '芜湖', '清远', '来宾', '石家庄', '定西', '福州', '黔东南苗族侗族自治州', '广元', '洛阳', '淄博', '临汾', '娄底', '鸡西', '北京', '沧州', '崇左', '海北藏族自治州', '贺州', '湖州', '三门峡', '临沂', '肇庆', '大理白族自治州', '咸宁', '徐州', '内江', '兰州', '唐山', '永州', '黔西南布依族苗族自治州', '韶关', '晋中', '遵义', '松原', '上海', '十堰', '乌海', '金昌', '商洛', '南阳', '六盘水', '汉中', '延边朝鲜族自治州', '锡林郭勒盟', '保定', '新余', '滨州']

fileNamePath = "F:\\01大连民族\\百度迁徙爬取和数据\\百度迁徙数据-final\\03将两个In和Out相同行合并_最终数据\\"
# 计算代数连通性
def diversity_value():
    diversity_superNode=[]
    for i in range(len(listXData)):
        # 循环画图
        try:
            filePathInMethon = fileNamePath + listXData[i] + "finalData.csv"
            G = drawpicture(filePathInMethon)
            for city_want in nodeList:
                G.add_edges_from([(city_want, "超级节点")])
            name = ['city_name', "city_name_another"]
            result_finall = G.edges()
            test = pd.DataFrame(columns=name, data=result_finall)  # 数据有er列，列名分别为one,two,three
            filename_path_param = "D:\\04python project\\01-爬虫-爬取百度迁徙数据\physicalconnecitvity\indicators\\" \
                                  "diversity\\" \
                                  "garbage\\" + listXData[i]+ "superNode.csv"
            test.to_csv(filename_path_param, index=False, encoding="utf-8-sig")
            # 调用R计算diversity内容
            t3 = robjects.r['get_diversity_value_list'](robjects.StrVector([filename_path_param]))

        except Exception as problem:
            print("(代数连通性) error打开迁徙文件出问题：", problem)
        else:
            diversity_superNode.append(t3[0])
    return diversity_superNode

print(diversity_value())





































