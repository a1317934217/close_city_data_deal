#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/19 15:09
# @Author  : wuhao
# @Email   : guess?????
# @File    : makebar.py
# -*- coding: utf-8 -*-
# import matplotlib.pyplot as plt
import csv

import networkx as nx
from matplotlib.font_manager import FontProperties

import matplotlib
from matplotlib import pyplot as plt
from collections import Counter
import os
import pandas as pd
#
filepath_front ="D:\\04python project\\01-爬虫-爬取百度迁徙数据\\physicalconnecitvity\\indicators\\data\\average_node_connectiy\\"
# filepath_front ="/Users/wuhao/PycharmProjects/Baidu_migrationData/physicalconnecitvity/indicators/data/"
filelist =['0101-0104data.csv', '0104-0106data.csv', '0106-0111data.csv', '0111-0116data.csv', '0116-0121data.csv', '0204-0207data.csv', '0207-0209data.csv', '0209-0212data.csv', '0212-0213data.csv', '0221-0222data.csv', '0222-0224data.csv', '0224-0227data.csv', '0227-0307data.csv', '0307-0315data.csv', '0315-0316data.csv']
# with open(filepath_front + "Counterdata.csv", 'r', encoding='utf-8')as f:
#     read = csv.reader(f)
#     for index, info in enumerate(read):

# 将全局的字体设置为黑体
# matplotlib.rcParams['font.family'] = '/Library/Fonts/Arial Unicode.ttf'

# 设置Mac上的字体（Mac上跑数据的时候）
font = FontProperties(fname='/Library/Fonts/Arial Unicode.ttf')




data0101_0104data= [('济南', 4), ('烟台', 2), ('石家庄', 6), ('唐山', 4), ('武汉', 10), ('十堰', 1), ('深圳', 8), ('上海', 15), ('沈阳', 2), ('长春', 5), ('重庆', 7), ('湘西土家族苗族自治州', 3), ('长沙', 6), ('北京', 15)]
data0104_0106data= [('榆林', 1), ('吕梁', 2), ('鄂尔多斯', 2), ('巴彦淖尔', 2), ('长治', 3), ('晋中', 1), ('张家口', 4), ('大同', 2), ('菏泽', 6), ('青岛', 1), ('乌兰察布', 4), ('包头', 1), ('忻州', 2), ('朔州', 1)]
data0106_0111data= [('乌兰察布', 3), ('包头', 2), ('鄂尔多斯', 1), ('巴彦淖尔', 2), ('榆林', 1), ('吕梁', 1), ('保定', 1), ('邯郸', 2), ('张家口', 4), ('大同', 2), ('佛山', 1), ('茂名', 1), ('济南', 3), ('日照', 2)]
data0111_0116data= [('清远', 2), ('东莞', 3), ('深圳', 8), ('湛江', 2), ('恩施土家族苗族自治州', 1), ('武汉', 5), ('茂名', 2), ('河源', 2), ('广州', 2), ('南宁', 1), ('苏州', 2), ('宿迁', 1), ('佛山', 2), ('厦门', 2)]
data0116_0121data= [('阜阳', 1), ('上海', 1), ('重庆', 8), ('深圳', 2), ('宿迁', 3), ('苏州', 1), ('恩施土家族苗族自治州', 1), ('武汉', 4), ('龙岩', 2), ('泉州', 1), ('自贡', 2), ('平凉', 2), ('兰州', 1), ('蚌埠', 2)]
data0204_0207data= [('上海', 1), ('南通', 2), ('张家口', 1), ('北京', 1), ('深圳', 2), ('梅州', 1), ('绍兴', 1), ('杭州', 2), ('成都', 2), ('自贡', 1), ('广元', 1), ('佛山', 1), ('肇庆', 1), ('南宁', 4)]

data0207_0209data= [('淄博', 2), ('滨州', 1), ('株洲', 2), ('湘潭', 2), ('衡阳', 2), ('郴州', 1), ('广州', 1), ('中山', 1), ('益阳', 2), ('常德', 1), ('岳阳', 1), ('南通', 1), ('盐城', 1), ('烟台', 1)]
data0209_0212data= [('广州', 3), ('湛江', 1), ('南充', 1), ('成都', 4), ('遂宁', 1), ('惠州', 1), ('乐山', 1), ('重庆', 4), ('达州', 2), ('宜春', 1), ('南昌', 1), ('株洲', 2), ('湘潭', 2), ('中山', 1)]
data0212_0213data= [('绍兴', 1), ('杭州', 1), ('宜春', 1), ('南昌', 1), ('南通', 1), ('盐城', 1), ('唐山', 1), ('秦皇岛', 1), ('淄博', 1), ('潍坊', 1), ('永州', 1), ('郴州', 1)]
data0221_0222data= [('杭州', 6), ('绍兴', 1), ('长春', 3), ('四平', 1), ('嘉兴', 1), ('郑州', 5), ('开封', 2), ('湖州', 1), ('镇江', 1), ('南京', 3), ('松原', 1), ('周口', 4), ('太原', 3), ('晋中', 1)]
data0222_0224data= [('苏州', 6), ('上海', 3), ('无锡', 2), ('长沙', 1), ('邵阳', 2), ('盐城', 1), ('西安', 2), ('宝鸡', 2), ('郑州', 2), ('商丘', 1), ('南通', 1), ('成都', 4), ('巴中', 1), ('娄底', 1)]
data0224_0227data= [('鞍山', 2), ('营口', 2), ('泉州', 1), ('三明', 1), ('周口', 3), ('开封', 1), ('广州', 1), ('珠海', 1), ('漯河', 2), ('邯郸', 1), ('石家庄', 1), ('洛阳', 2), ('三门峡', 1), ('宁波', 1)]

data0227_0307data= [('邯郸', 2), ('石家庄', 1), ('厦门', 2), ('龙岩', 2), ('济南', 3), ('菏泽', 3), ('郑州', 3), ('驻马店', 5), ('西安', 3), ('安康', 1), ('济宁', 2), ('保定', 3), ('廊坊', 2), ('茂名', 2)]
data0307_0315data= [('四平', 2), ('长春', 4), ('潍坊', 3), ('青岛', 5), ('郑州', 3), ('新乡', 4), ('济南', 3), ('泰安', 3), ('烟台', 1), ('嘉兴', 3), ('上海', 6), ('吉林', 1), ('松原', 1), ('临沂', 9)]
data0315_0316data= [('上海', 4), ('常州', 1), ('徐州', 2), ('南京', 3), ('南昌', 1), ('吉安', 1), ('泰州', 1), ('大庆', 1), ('哈尔滨', 2), ('北海', 1), ('南宁', 1), ('广州', 1), ('河源', 1), ('沈阳', 2)]




list_name_Y = [data0101_0104data,data0104_0106data,data0106_0111data,data0111_0116data,data0116_0121data,data0204_0207data,
               data0207_0209data,data0209_0212data,data0212_0213data,data0221_0222data,data0222_0224data,data0224_0227data,
               data0227_0307data,data0307_0315data,data0315_0316data]

# for i  in list_name_Y:
#     list_cityname = []
#     list_cityvalue=[]
#     for j in i:
#         list_cityname.append(j[0])
#         list_cityvalue.append(j[1])
#     plt.bar(list_cityname, list_cityvalue,  tick_label = list_cityname, fc='r') #label='边数量'
#     plt.xticks(list_cityname, rotation=45, fontproperties=font)
#     plt.ylabel("数值", fontproperties=font)
#     # plt.title(fontproperties=font)
#
#     plt.legend()
#     plt.show()


# from matplotlib.font_manager import FontManager
# fm = FontManager()
# mat_fonts = set(f.name for f in fm.ttflist)
# print(mat_fonts)


remove_edge_list_diffedge =["0101_0102data_falling.csv","0104_0105data_falling.csv","0109_0110data_risiing.csv","0115_0116data_risiing.csv","0118_0119data_falling.csv","0121_0122data_risiing.csv","0122_0123data_falling.csv","0102_0103data_risiing.csv","0110_0111data_falling.csv"]
remove_edge_list_origionnet = ["20200101finalData.csv","20200104finalData.csv","20200109finalData.csv" ,"20200115finalData.csv","20200118finalData.csv","20200121finalData.csv","20200122finalData.csv","20200102finalData.csv","20200110finalData.csv"]

add_edge_list_diffedge = []
add_edge_list_origionnet =[]

list_a = [4,5,6,1]
list_b = [1,2,3]
# 列表b中包含而列表A中没有的元素
# differ_list_b = list(set(list_b).difference(set(list_a)))
# print(differ_list_b)
# # 列表a中包含而列表b中没有的元素
# differ_list_a = list(set(list_a).difference(set(list_b)))
# print(differ_list_a)

# dataMiga_add = pd.read_csv(filepath_front + '0102-0103data_removeEdges.csv')
# print(dataMiga_add)
# if len(dataMiga_add)==0:
#     print("adawdasdawdas")
# else:
#     print("meiyou")
# print(len(dataMiga_add)==0)
# aaaa = 1.4849956587801172
# a=('%.5f' % aaaa)
# print(a)



result_filename  = ['0101-0102data_addEdges.cs_finall_indicators.csv', '0101-0102data_removeEdges_finall_indicators.csv', '0102-0103data_addEdges.cs_finall_indicators.csv', '0103-0104data_addEdges.cs_finall_indicators.csv', '0103-0104data_removeEdges_finall_indicators.csv', '0104-0105data_addEdges.cs_finall_indicators.csv', '0104-0105data_removeEdges_finall_indicators.csv', '0107-0108data_addEdges.cs_finall_indicators.csv', '0107-0108data_removeEdges_finall_indicators.csv', '0110-0111data_addEdges.cs_finall_indicators.csv', '0110-0111data_removeEdges_finall_indicators.csv', '0111-0112data_addEdges.cs_finall_indicators.csv', '0111-0112data_removeEdges_finall_indicators.csv', '0120-0121data_addEdges.cs_finall_indicators.csv', '0120-0121data_removeEdges_finall_indicators.csv', '0121-0122data_addEdges.cs_finall_indicators.csv', '0121-0122data_removeEdges_finall_indicators.csv']
adawdawdas = '0101-0102data_removeEdges_finall_indicators.csv'
# print(adawdawdas[0:9])
# print(adawdawdas[14:15])
# print(adawdawdas[0:4])














average_node_result_Edges_fileFront = "D:\\04python project\\01-爬虫-爬取百度迁徙数据\\physicalconnecitvity\\indicators\\data\\diversity"
# print(os.listdir(average_node_result_Edges_fileFront))


















fileNamePath = "F:\\01大连民族\\百度迁徙爬取和数据\\百度迁徙数据-final\\03将两个In和Out相同行合并_最终数据\\"

# 根据路径画图
def drawpicture(filePath):
    """
    输入文件路径最后绘制成图G
    """
    G = nx.DiGraph()
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
def drawpicture_underect(filePath):
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

listXData = ['20200101', '20200102', '20200103', '20200104', '20200105', '20200106', '20200107', '20200108', '20200109', '20200110', '20200111', '20200112', '20200113', '20200114', '20200115', '20200116', '20200117', '20200118', '20200119', '20200120', '20200121', '20200122', '20200123', '20200124', '20200125', '20200126', '20200127', '20200128', '20200129', '20200130', '20200131', '20200201', '20200202', '20200203', '20200204', '20200205', '20200206', '20200207', '20200208', '20200209', '20200210', '20200211', '20200212', '20200213', '20200214', '20200215', '20200216', '20200217', '20200218', '20200219', '20200220', '20200221', '20200222', '20200223', '20200224', '20200225', '20200226', '20200227', '20200228', '20200229', '20200301', '20200302', '20200303', '20200304', '20200305', '20200306', '20200307', '20200308', '20200309', '20200310', '20200311', '20200312', '20200313', '20200314', '20200315', '20200316', '20200317', '20200318', '20200319', '20200320', '20200321', '20200322', '20200323', '20200324', '20200325', '20200326', '20200327', '20200328', '20200329', '20200330', '20200331', '20200401', '20200402', '20200403', '20200404', '20200405', '20200406', '20200407', '20200408', '20200409', '20200410', '20200411', '20200412', '20200413', '20200414', '20200415', '20200416', '20200417', '20200418', '20200419', '20200420', '20200421', '20200422', '20200423', '20200424', '20200425', '20200426', '20200427', '20200428', '20200429', '20200430', '20200501', '20200502', '20200503']
list_number_connect=[]
list_weaker_number=[]
# for i in listXData:
#     G = drawpicture(fileNamePath +i+"finalData.csv")
#     G_under = drawpicture_underect(fileNamePath +i+"finalData.csv")
#     list_weaker_number.append(nx.number_weakly_connected_components(G))
#     #最大连通子图
#     ccc = max(nx.connected_components(G_under), key=len)
#     list_number_connect.append(len(ccc))
# #511
# print(list_number_connect)
# print(list_weaker_number)
number_weakly_connected_component_list= [1, 2, 11, 19, 26, 36, 48, 65, 78, 92, 104, 111, 122, 133, 139, 152, 161, 170, 182, 187, 193, 198, 206, 217, 225, 230, 231, 236, 239, 245, 251, 255, 260, 264, 271, 273, 274, 277, 281, 283, 286, 286, 288, 289, 290, 293, 300, 303, 303, 307, 309]
# print(len(number_weakly_connected_component_list))

# print(nx.weakly_connected_components(G))

file_path_average_node = ['0101_0102data_falling.csv', '0102_0103data_risiing.csv', '0103_0104data_risiing.csv', '0104_0105data_falling.csv', '0107_0108data_risiing.csv', '0110_0111data_risiing.csv', '0111_0112data_falling.csv', '0120_0121data_risiing.csv', '0121_0122data_falling.csv']
# 输出前十四个城市的增加或减少的 连边
# for file_name in filelist:
#     list_value =[]
#     with open(filepath_front + file_name, 'r', encoding='utf-8')as f:
#         read = csv.reader(f)
#         for index, info in enumerate(read):
#             if index != 0:  # 这里加判断
#                 # print(info[:2])
#                 list_value.append(info[0])
#                 list_value.append(info[1])
#         counter_value = Counter(list_value)
#         print(counter_value)
        # print(file_name,list(dict(counter_value).items())[:14])

# finall = {'周口-阜阳': 1.481929672237899, '赤峰-朝阳': 1.4820110701107012, '徐州-枣庄': 1.485891035380942, '榆林-吕梁': 1.486216626872151, '徐州-济宁': 1.486732146733232, '钦州-防城港': 1.4868949424788365, '榆林-忻州': 1.4867050141089646, '盐城-连云港': 1.4852669850227913, '聊城-邢台': 1.4819025396136314, '宜春-新余': 1.4799218580421099, '镇江-扬州': 1.4862980247449533, '葫芦岛-秦皇岛': 1.4170284349902322, '六盘水-黔西南布依族苗族自治州': 1.4866236162361623, '黄冈-九江': 1.4529791621445627, '六盘水-安顺': 1.486922075103104, '潍坊-日照': 1.4851313219014544, '漯河-周口': 1.4868678098545691, '衡水-邢台': 1.4864879531148252, '商丘-菏泽': 1.4815226828738877, '南充-广安': 1.4868678098545691, '宿迁-连云港': 1.4852127197742566, '益阳-岳阳': 1.4868949424788365, '聊城-邯郸': 1.486732146733232, '铜仁-重庆': 1.4865693509876274, '通辽-赤峰': 1.4820110701107012, '潮州-揭阳': 1.4820110701107012, '清远-韶关': 1.4865693509876274, '长沙-萍乡': 1.4799218580421099, '益阳-常德': 1.4868949424788365, '遂宁-绵阳': 1.472297590622965, '漯河-平顶山': 1.4868678098545691, '佛山-珠海': 1.486732146733232, '重庆-资阳': 1.4868678098545691, '驻马店-周口': 1.4867864119817669, '南京-芜湖': 1.4869492077273714, '驻马店-南阳': 1.4849956587801172, '鞍山-盘锦': 1.4868406772303018, '南阳-平顶山': 1.4849956587801172, '内江-资阳': 1.4868678098545691, '娄底-湘潭': 1.4771271977425657, '焦作-洛阳': 1.4709138267853268, '常州-泰州': 1.4866778814846973, '宿州-蚌埠': 1.4824451920989798, '清远-东莞': 1.4862980247449533, '嘉兴-绍兴': 1.486732146733232, '永州-衡阳': 1.4820110701107012, '焦作-济源': 1.4799218580421099, '黔南布依族苗族自治州-安顺': 1.4864608204905578, '张家口-大同': 1.4814684176253528, '忻州-朔州': 1.4817397438680269, '周口-许昌': 1.4867864119817669, '安顺-黔西南布依族苗族自治州': 1.4866236162361623, '安庆-池州': 1.4799218580421099, '徐州-连云港': 1.4861080963750815, '盘锦-营口': 1.4868406772303018, '通辽-沈阳': 1.4820110701107012, '恩施土家族苗族自治州-湘西土家族苗族自治州': 1.4799218580421099, '上饶-鹰潭': 1.4799218580421099, '铁岭-四平': 1.4672780551334925, '晋中-临汾': 1.4862437594964184, '大同-乌兰察布': 1.4624755806381593, '镇江-无锡': 1.486596483611895, '衡阳-株洲': 1.4675222487518993, '遵义-黔南布依族苗族自治州': 1.4867864119817669, '茂名-玉林': 1.4864608204905578, '常德-张家界': 1.4799218580421099, '西安-运城': 1.4861352289993488, '湛江-玉林': 1.4865693509876274, '荆州-潜江': 1.4799218580421099, '宣城-南京': 1.485185587149989, '达州-巴中': 1.4820110701107012, '铜仁-黔东南苗族侗族自治州': 1.486270892120686, '东莞-江门': 1.486732146733232, '定西-临夏回族自治州': 1.486922075103104, '深圳-江门': 1.4868135446060342, '淄博-东营': 1.4851584545257217, '德州-滨州': 1.47644888213588, '滁州-扬州': 1.4852669850227913, '商丘-亳州': 1.4823095289776427, '曲靖-红河哈尼族彝族自治州': 1.472297590622965, '周口-开封': 1.4851313219014544, '龙岩-漳州': 1.4868135446060342, '梧州-贵港': 1.4728945083568483, '白城-松原': 1.486922075103104, '白城-兴安盟': 1.4799218580421099, '贺州-梧州': 1.4799218580421099}
# aaaaaa = sorted(finall.items(),key = lambda x:x[1],reverse = True)
# print(aaaaaa)

result = [('南京-芜湖', 1.4869492077273714), ('六盘水-安顺', 1.486922075103104), ('定西-临夏回族自治州', 1.486922075103104), ('白城-松原', 1.486922075103104), ('钦州-防城港', 1.4868949424788365), ('益阳-岳阳', 1.4868949424788365), ('益阳-常德', 1.4868949424788365), ('漯河-周口', 1.4868678098545691), ('南充-广安', 1.4868678098545691), ('漯河-平顶山', 1.4868678098545691), ('重庆-资阳', 1.4868678098545691), ('内江-资阳', 1.4868678098545691), ('鞍山-盘锦', 1.4868406772303018), ('盘锦-营口', 1.4868406772303018), ('深圳-江门', 1.4868135446060342), ('龙岩-漳州', 1.4868135446060342), ('驻马店-周口', 1.4867864119817669), ('周口-许昌', 1.4867864119817669), ('遵义-黔南布依族苗族自治州', 1.4867864119817669), ('徐州-济宁', 1.486732146733232), ('聊城-邯郸', 1.486732146733232), ('佛山-珠海', 1.486732146733232), ('嘉兴-绍兴', 1.486732146733232), ('东莞-江门', 1.486732146733232), ('榆林-忻州', 1.4867050141089646), ('常州-泰州', 1.4866778814846973), ('六盘水-黔西南布依族苗族自治州', 1.4866236162361623), ('安顺-黔西南布依族苗族自治州', 1.4866236162361623), ('镇江-无锡', 1.486596483611895), ('铜仁-重庆', 1.4865693509876274), ('清远-韶关', 1.4865693509876274), ('湛江-玉林', 1.4865693509876274), ('衡水-邢台', 1.4864879531148252), ('黔南布依族苗族自治州-安顺', 1.4864608204905578), ('茂名-玉林', 1.4864608204905578), ('镇江-扬州', 1.4862980247449533), ('清远-东莞', 1.4862980247449533), ('铜仁-黔东南苗族侗族自治州', 1.486270892120686), ('晋中-临汾', 1.4862437594964184), ('榆林-吕梁', 1.486216626872151), ('西安-运城', 1.4861352289993488), ('徐州-连云港', 1.4861080963750815), ('徐州-枣庄', 1.485891035380942), ('盐城-连云港', 1.4852669850227913), ('滁州-扬州', 1.4852669850227913), ('宿迁-连云港', 1.4852127197742566), ('宣城-南京', 1.485185587149989), ('淄博-东营', 1.4851584545257217), ('潍坊-日照', 1.4851313219014544), ('周口-开封', 1.4851313219014544), ('驻马店-南阳', 1.4849956587801172), ('南阳-平顶山', 1.4849956587801172), ('宿州-蚌埠', 1.4824451920989798), ('商丘-亳州', 1.4823095289776427), ('赤峰-朝阳', 1.4820110701107012), ('通辽-赤峰', 1.4820110701107012), ('潮州-揭阳', 1.4820110701107012), ('永州-衡阳', 1.4820110701107012), ('通辽-沈阳', 1.4820110701107012), ('达州-巴中', 1.4820110701107012), ('周口-阜阳', 1.481929672237899), ('聊城-邢台', 1.4819025396136314), ('忻州-朔州', 1.4817397438680269), ('商丘-菏泽', 1.4815226828738877), ('张家口-大同', 1.4814684176253528), ('宜春-新余', 1.4799218580421099), ('长沙-萍乡', 1.4799218580421099), ('焦作-济源', 1.4799218580421099), ('安庆-池州', 1.4799218580421099), ('恩施土家族苗族自治州-湘西土家族苗族自治州', 1.4799218580421099), ('上饶-鹰潭', 1.4799218580421099), ('常德-张家界', 1.4799218580421099), ('荆州-潜江', 1.4799218580421099), ('白城-兴安盟', 1.4799218580421099), ('贺州-梧州', 1.4799218580421099), ('娄底-湘潭', 1.4771271977425657), ('德州-滨州', 1.47644888213588), ('梧州-贵港', 1.4728945083568483), ('遂宁-绵阳', 1.472297590622965), ('曲靖-红河哈尼族彝族自治州', 1.472297590622965), ('焦作-洛阳', 1.4709138267853268), ('衡阳-株洲', 1.4675222487518993), ('铁岭-四平', 1.4672780551334925), ('大同-乌兰察布', 1.4624755806381593), ('黄冈-九江', 1.4529791621445627), ('葫芦岛-秦皇岛', 1.4170284349902322)]
# name=['one',"awd"]
# test=pd.DataFrame(columns=name,data=result)#数据有三列，列名分别为one,two,three
# print(test)
# test.to_csv('D:\\04python project\\01-爬虫-爬取百度迁徙数据\physicalconnecitvity\indicators\data\\average_node_connectiy\\'
#             '123.csv',)index=False, encoding="utf-8-sig"
# ccccc  = "0101_0102data_falling.csv"
# print(ccccc[:21])



#'武汉': 7, '上海': 7, '合肥': 7, '北京': 7, '西安
# list_aaaa = ['信阳-武汉', '西安-武汉', '西安-天水', '武汉-三门峡', '周口-阜阳']
# for edge_name_want in list_aaaa:
#     print(edge_name_want.find("武汉"))









# url = "http://www.6mm.cc/uploads/allimg/1306/2-13060F12S3.jpg"
# url ='信阳-武汉'
# print(url.rfind('-', 1))
# print(url[0:url.rfind('-', 1)])
# print(url[url.rfind('-', 1)+1:])


import collections
#寻找城市的连边数量 返回Counter()
def find_city_Counter(edges_add_list,first_name,second_name):
    # for row in df.iterrows():
    list_new_data =[]
    for row in edges_add_list.iterrows():
        list_new_data.append(row[1][first_name])
        list_new_data.append(row[1][second_name])
    count=collections.Counter(list_new_data)
    #{'武汉': 7, '上海': 7, '合肥': 7,}
    return count

first_name_remove = "city_name_remove"
second_name_remove = "city_id_name_remove"
first_name_add = "city_name_add"
second_name_add = "city_id_name_add"
fileName_end = "0315-0316data_removeEdges.csv"   #addEdges   #removeEdges
cityname =['萍乡','广州']   #['上海', '北京', '苏州', '武汉']
filename_path_param = "D:\\04python project\\01-爬虫-爬取百度迁徙数据\physicalconnecitvity\indicators\data\\finall_data\\"+fileName_end
if fileName_end[14:15] == "r":
    add_edges_data = pd.read_csv(filename_path_param)
    print(find_city_Counter(add_edges_data,first_name_remove,second_name_remove))

    for city_name_remove_want in cityname:
        list_city_name = []
        for edge_name_want in add_edges_data.iterrows():
            # print(edge_name_want)
            if edge_name_want[1][first_name_remove] == city_name_remove_want or edge_name_want[1][second_name_remove] == city_name_remove_want:
                list_city_name.append(
                    edge_name_want[1][first_name_remove] + "-" + edge_name_want[1][second_name_remove])
        print(city_name_remove_want,list_city_name)
elif fileName_end[14:15] == "a":
    add_edges_data = pd.read_csv(filename_path_param)
    print(find_city_Counter(add_edges_data, first_name_add, second_name_add))
    for city_name_remove_want in cityname:
        list_city_name = []
        for edge_name_want in add_edges_data.iterrows():
            # print(edge_name_want)
            if edge_name_want[1][first_name_add] == city_name_remove_want or edge_name_want[1][second_name_add] == city_name_remove_want:
                list_city_name.append(
                    edge_name_want[1][first_name_add] + "-" + edge_name_want[1][second_name_add])
        print(city_name_remove_want,list_city_name)
