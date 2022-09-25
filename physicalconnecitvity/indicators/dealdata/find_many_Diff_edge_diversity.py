#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/21 19:12
# @Author  : wuhao
# @Email   : guess?????
# @File    : find_diff_edges_average_diversity.py
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import csv
import networkx as nx
import pandas as pd
import collections
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
#寻找城市的连边数量 返回Counter()
def find_city_Counter(edges_add_list):
    # for row in df.iterrows():
    list_new_data =[]
    for row in edges_add_list.iterrows():
        list_new_data.append(row[1][0])
        list_new_data.append(row[1][1])
    count=collections.Counter(list_new_data)
    #{'武汉': 7, '上海': 7, '合肥': 7,}
    return count

fileNamePath_one = "F:\\01大连民族\\百度迁徙爬取和数据\\百度迁徙数据-final\\03将两个In和Out相同行合并_最终数据\\"
average_node_result_Edges_fileFront = "D:\\04python project\\01-爬虫-爬取百度迁徙数据\\physicalconnecitvity\\indicators\\data\\diversity\\"
result_filename = ['0101-0102data_addEdges.csv', '0101-0102data_removeEdges.csv', '0102-0103data_addEdges.csv', '0102-0103data_removeEdges.csv', '0104-0105data_addEdges.csv', '0104-0105data_removeEdges.csv', '0109-0110data_addEdges.csv', '0109-0110data_removeEdges.csv', '0110-0111data_addEdges.csv', '0110-0111data_removeEdges.csv', '0115-0116data_addEdges.csv', '0115-0116data_removeEdges.csv', '0118-0119data_addEdges.csv', '0118-0119data_removeEdges.csv', '0121-0122data_addEdges.csv', '0121-0122data_removeEdges.csv', '0122-0123data_addEdges.csv', '0122-0123data_removeEdges.csv']
#增加连边计算平均点连通性
def useCity_addEdges_Tocaculate_diversity(city_name,add_edges,G_contrast,fileName_date):
    """
    使用边列表和城市名 计算增加某一天网络的连边 计算平均点连通性  保留两位小数
    :param city_name: 城市
    :param add_edges: 列表 dataformat
    :return:
    """
    global t3
    for edge_name_want in add_edges.iterrows():
        # print(edge_name_want)
        if edge_name_want[1][0] == city_name  or edge_name_want[1][1] ==city_name:
            G_contrast.add_edges_from([(edge_name_want[1][0], edge_name_want[1][1])])
        name=['city_name',"city_name_another"]
        result_finall = G_contrast.edges()
        test=pd.DataFrame(columns=name,data=result_finall)#数据有er列，列名分别为one,two,three
        filename_path_param = "D:\\04python project\\01-爬虫-爬取百度迁徙数据\physicalconnecitvity\indicators\data\\diversity\\" \
                              "garbage\\"+fileName_date+city_name+"addEdges.csv"
        test.to_csv(filename_path_param,index=False, encoding="utf-8-sig")
        #调用R计算diversity内容
        t3=robjects.r['get_diversity_value_list'](robjects.StrVector([filename_path_param]))
    return t3[0]
#减少连边计算diversity
def userCity_removeEdges_Tocaculate_diversity(city_name,add_edges,G_contrast,fileName_date):
    """
    使用边列表和城市名 计算减少某一天网络的连边 计算平均点连通性  保留两位小数
    :param city_name: 城市
    :param add_edges: 列表
    :return:
    """
    global diversity_value
    for edge_name_want in add_edges.iterrows():
        if edge_name_want[1][0] == city_name  or edge_name_want[1][1] == city_name:
            G_contrast.remove_edges_from([(edge_name_want[1][0], edge_name_want[1][1])])
        #技术没突破，使用生成缓存csv 在用R读取的方式计算diversity
        name = ['city_name', "city_name_another"]
        result_finall = G_contrast.edges()
        test = pd.DataFrame(columns=name, data=result_finall)  # 数据有er列，列名分别为one,two,three
        filename_path_param = "D:\\04python project\\01-爬虫-爬取百度迁徙数据\physicalconnecitvity\indicators\data\\diversity\\" \
                              "garbage\\" + fileName_date + city_name + "removeEdges.csv"
        test.to_csv(filename_path_param, index=False, encoding="utf-8-sig")
        # 调用R计算diversity内容
        diversity_value = robjects.r['get_diversity_value_list'](robjects.StrVector([filename_path_param]))
    return diversity_value[0]

def tocsv_mutipul_edges(result_filename):
    field_order_move_in = ["city_name", "indicator_value", "edgenum"]
    for result_filename_one in result_filename:
        G_contrast = drawpicture(fileNamePath_one + "2020"+result_filename_one[0:4]+"finalData.csv")
        if result_filename_one[14:15] == "a":
            add_edges_data = pd.read_csv(average_node_result_Edges_fileFront+result_filename_one,skiprows=1)
            count_add = find_city_Counter(add_edges_data)
            with open(average_node_result_Edges_fileFront +"result\\multiple_cityedge_diversity\\" + result_filename_one[0:9]+"addEdgesValue.csv" , 'w', encoding="utf-8", newline='') as csvfile:
                writer = csv.DictWriter(csvfile, field_order_move_in)
                writer.writeheader()
                # dict_cite_value = {}
                for city_name_need_run in count_add.most_common():
                    # print(city_name_need_run[0], city_name_need_run[1])
                    final_value = useCity_addEdges_Tocaculate_diversity(city_name_need_run[0],add_edges_data,G_contrast,result_filename_one[0:9])
                    # dict_cite_value[city_name_need_run] = final_value
                    # sorted(dict_cite_value.items(), key=lambda x: x[1], reverse=True)
                    row = {"city_name": city_name_need_run[0], "indicator_value": final_value, "edgenum": city_name_need_run[1]}
                    writer.writerow(row)
            df = pd.read_csv(average_node_result_Edges_fileFront +"result\\multiple_cityedge_diversity\\" + result_filename_one[0:9]+"addEdgesValue.csv" )
            df.sort_values(by="indicator_value",ascending=False)
        elif result_filename_one[14:15] == "r":
            remove_edges_data = pd.read_csv(average_node_result_Edges_fileFront + result_filename_one,skiprows=1)
            count_remove = find_city_Counter(remove_edges_data)
            with open(average_node_result_Edges_fileFront +"result\\multiple_cityedge_diversity\\" + result_filename_one[0:9]+"removeEdgesValue.csv" , 'w', encoding="utf-8", newline='') as csvfile:
                writer = csv.DictWriter(csvfile, field_order_move_in)
                writer.writeheader()
                # dict_cite_value = {}
                for city_name_need_run in count_remove.most_common():
                    # print(city_name_need_run[0], city_name_need_run[1])
                    final_value = userCity_removeEdges_Tocaculate_diversity(city_name_need_run[0],remove_edges_data,G_contrast, result_filename_one[0:9])
                    # dict_cite_value[city_name_need_run] = final_value
                    # sorted(dict_cite_value.items(), key=lambda x: x[1], reverse=True)
                    row = {"city_name": city_name_need_run[0], "indicator_value": final_value, "edgenum": city_name_need_run[1]}
                    writer.writerow(row)
            df = pd.read_csv(average_node_result_Edges_fileFront + "result\\multiple_cityedge_diversity\\" + result_filename_one[0:9] + "removeEdgesValue.csv")
            df.sort_values(by="indicator_value", ascending=False)

# tocsv_mutipul_edges(result_filename)

# add_edges_data = pd.read_csv(average_node_result_Edges_fileFront+'0101-0102data_addEdges.csv',skiprows=1)
# for row in add_edges_data.iterrows():
#     # print(row[0])
#     print(row[1][0])
#     print(row[1][1])
nodeList=['舟山', '贵阳', '黄石', '昭通', '焦作', '南通', '丽水', '晋城', '巴中', '阜新', '合肥', '威海', '宿州', '德阳', '白山', '延安', '攀枝花', '佛山', '亳州', '天门', '濮阳', '池州', '漯河', '盐城', '厦门', '丹东', '保山', '贵港', '南昌', '绵阳', '黄冈', '廊坊', '鄂州', '渭南', '宣城', '乐山', '昆明', '淮安', '云浮', '南京', '长治', '防城港', '鞍山', '泸州', '大连', '阳泉', '盘锦', '温州', '赣州', '荆门', '西宁', '湘西土家族苗族自治州', '吉安', '开封', '铜陵', '孝感', '呼和浩特', '佳木斯', '枣庄', '眉山', '遂宁', '武汉', '许昌', '达州', '青岛', '承德', '咸阳', '驻马店', '天水', '苏州', '长春', '黑河', '连云港', '红河哈尼族彝族自治州', '辽阳', '六安', '菏泽', '衡水', '营口', '兴安盟', '岳阳', '黔南布依族苗族自治州', '湘潭', '泉州', '齐齐哈尔', '平顶山', '武威', '宜昌', '滁州', '江门', '临沧', '玉溪', '郴州', '葫芦岛', '沈阳', '商丘', '潜江', '南充', '嘉兴', '东莞', '广安', '恩施土家族苗族自治州', '乌兰察布', '潍坊', '襄阳', '天津', '茂名', '大庆', '邢台', '镇江', '张掖', '河源', '东营', '绥化', '马鞍山', '台州', '抚顺', '柳州', '西双版纳傣族自治州', '西安', '白银', '蚌埠', '揭阳', '宜春', '九江', '邵阳', '阜阳', '四平', '张家口', '湛江', '铁岭', '德宏傣族景颇族自治州', '普洱', '荆州', '伊春', '济宁', '烟台', '珠海', '太原', '本溪', '惠州', '无锡', '双鸭山', '安阳', '运城', '衡阳', '广州', '玉林', '淮北', '凉山彝族自治州', '自贡', '常德', '海南藏族自治州', '长沙', '宁德', '呼伦贝尔', '百色', '新乡', '包头', '甘孜藏族自治州', '朔州', '辽源', '海西蒙古族藏族自治州', '张家界', '重庆', '庆阳', '聊城', '泰州', '上饶', '曲靖', '郑州', '中山', '安顺', '白城', '漳州', '淮南', '桂林', '南宁', '益阳', '济源', '文山壮族苗族自治州', '北海', '抚州', '阳江', '秦皇岛', '梅州', '成都', '德州', '锦州', '安康', '巴彦淖尔', '河池', '汕头', '通化', '龙岩', '梧州', '宜宾', '莆田', '济南', '安庆', '萍乡', '深圳', '日照', '赤峰', '宁波', '平凉', '邯郸', '丽江', '大同', '汕尾', '株洲', '宿迁', '怀化', '钦州', '哈尔滨', '南平', '宝鸡', '鹤岗', '榆林', '通辽', '随州', '泰安', '鹤壁', '朝阳', '资阳', '雅安', '仙桃', '信阳', '楚雄彝族自治州', '潮州', '绍兴', '周口', '常州', '吕梁', '忻州', '景德镇', '三明', '鹰潭', '杭州', '金华', '鄂尔多斯', '衢州', '牡丹江', '陇南', '铜川', '扬州', '临夏回族自治州', '阿坝藏族羌族自治州', '芜湖', '清远', '来宾', '石家庄', '定西', '福州', '黔东南苗族侗族自治州', '广元', '洛阳', '淄博', '临汾', '娄底', '鸡西', '北京', '沧州', '崇左', '海北藏族自治州', '贺州', '湖州', '三门峡', '临沂', '肇庆', '大理白族自治州', '咸宁', '徐州', '内江', '兰州', '唐山', '永州', '黔西南布依族苗族自治州', '韶关', '晋中', '遵义', '松原', '上海', '十堰', '乌海', '金昌', '商洛', '南阳', '六盘水', '汉中', '延边朝鲜族自治州', '锡林郭勒盟', '保定', '新余', '滨州']

def drawpicture_new(filePath):
    """
    输入文件路径最后绘制成图G
    """
    G = nx.Graph()
    G.add_nodes_from(nodeList)
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

G_demo_one = drawpicture(fileNamePath_one+"20200101finalData.csv")
print("G_demo_one:",len(G_demo_one.edges()))
print("G_demo_one:",len(G_demo_one.nodes()))
G_demo_two = drawpicture_new(fileNamePath_one+"20200101finalData.csv")
print("G_demo_two:",len(G_demo_two.edges()))
print("G_demo_two:",len(G_demo_two.nodes()))


