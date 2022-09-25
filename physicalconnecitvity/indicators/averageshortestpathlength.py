#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 15:52
# @Author  : wuhao
# @Email   : guess?????
# @File    : averageshortestpathlength.py
# 平均最短路径长度

import datetime

import matplotlib
import networkx as nx
import numpy as np
import pandas as pd
# coding=utf-8
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import FuncFormatter, MaxNLocator
from networkx.algorithms.connectivity import local_node_connectivity

# 多重边无向图
# coding=utf-8
# 多重边无向图
# listXData = ['20200101', '20200102', '20200103', '20200104', '20200105', '20200106', '20200107', '20200108', '20200109', '20200110', '20200111', '20200112', '20200113', '20200114', '20200115', '20200116', '20200117', '20200118', '20200119', '20200120', '20200121', '20200122', '20200123', '20200124', '20200125', '20200126', '20200127', '20200128', '20200129', '20200130', '20200131', '20200201', '20200202', '20200203', '20200204', '20200205', '20200206', '20200207', '20200208', '20200209', '20200210', '20200211', '20200212', '20200213', '20200214', '20200215', '20200216', '20200217', '20200218', '20200219', '20200220', '20200221', '20200222', '20200223', '20200224', '20200225', '20200226', '20200227', '20200228', '20200229', '20200301', '20200302', '20200303', '20200304', '20200305', '20200306', '20200307', '20200308', '20200309', '20200310', '20200311', '20200312', '20200313', '20200314', '20200315', '20200316', '20200317', '20200318', '20200319', '20200320', '20200321', '20200322', '20200323', '20200324', '20200325', '20200326', '20200327', '20200328', '20200329', '20200330', '20200331', '20200401', '20200402', '20200403', '20200404', '20200405', '20200406', '20200407', '20200408', '20200409', '20200410', '20200411', '20200412', '20200413', '20200414', '20200415', '20200416', '20200417', '20200418', '20200419', '20200420', '20200421', '20200422', '20200423', '20200424', '20200425', '20200426', '20200427', '20200428', '20200429', '20200430', '20200501', '20200502', '20200503', '20201001', '20201002', '20201003', '20201004', '20201005', '20201006', '20201007', '20201008', '20201009', '20201010', '20201011', '20201012', '20201013', '20201014', '20201015', '20201016', '20201017', '20201018', '20201019', '20201020', '20201021', '20201022', '20201023', '20201024', '20201025', '20201026', '20201027', '20201028', '20201029', '20201030', '20201031', '20201101', '20201102', '20201103', '20201104', '20201105', '20201106', '20201107', '20201108', '20201109', '20201110', '20201111', '20201112', '20201113', '20201114', '20201115', '20201116', '20201117', '20201118', '20201119', '20201120', '20201121', '20201122', '20201123', '20201124', '20201125', '20201126', '20201127', '20201128', '20201129', '20201130', '20201201', '20201202', '20201203', '20201204', '20201205', '20201206', '20201207', '20201208', '20201209', '20201210', '20201211', '20201212', '20201213', '20201214', '20201215', '20201216', '20201217', '20201218', '20201219', '20201220', '20201221', '20201222', '20201223', '20201224', '20201225', '20201226', '20201227', '20201228', '20201229', '20201230', '20201231', '20210101', '20210102', '20210103', '20210104', '20210105', '20210106', '20210107', '20210108', '20210109', '20210110', '20210111', '20210112', '20210113', '20210114', '20210115', '20210116', '20210117', '20210118', '20210119', '20210120', '20210121', '20210122', '20210123', '20210124', '20210125', '20210126', '20210127', '20210128', '20210129', '20210130', '20210131', '20210201', '20210202', '20210203', '20210204', '20210205', '20210206', '20210207', '20210208', '20210209', '20210210', '20210211', '20210212', '20210213', '20210214', '20210215', '20210216', '20210217', '20210218', '20210219', '20210220', '20210221', '20210222', '20210223', '20210224', '20210225', '20210226', '20210227', '20210228', '20210301', '20210302', '20210303', '20210304', '20210305', '20210306', '20210307', '20210308', '20210309', '20210310', '20210311', '20210312', '20210313', '20210314', '20210315', '20210316', '20210317', '20210318', '20210319', '20210320', '20210321', '20210322', '20210323', '20210324', '20210325', '20210326', '20210327', '20210328', '20210329', '20210330', '20210331', '20210401', '20210402', '20210403', '20210404', '20210405', '20210406', '20210407', '20210408', '20210409', '20210410', '20210411', '20210412', '20210413', '20210414', '20210415', '20210416', '20210417', '20210418', '20210419', '20210420', '20210421', '20210422', '20210423', '20210424', '20210425', '20210426', '20210427', '20210428', '20210429', '20210430', '20210501', '20210502', '20210503', '20210504', '20210505', '20210506', '20210507', '20210508', '20210509', '20210510', '20210511', '20210512', '20210513', '20210514', '20210515', '20210516', '20210517', '20210518', '20210519', '20210520', '20210521', '20210522', '20210523', '20210524', '20210525', '20210526', '20210527', '20210528', '20210529', '20210530', '20210531', '20210601', '20210602', '20210603', '20210604', '20210605', '20210606', '20210607', '20210608', '20210609', '20210610', '20210611', '20210612', '20210613', '20210614', '20210615', '20210616', '20210617', '20210618', '20210619', '20210620', '20210621', '20210622', '20210623', '20210624', '20210625', '20210626', '20210627', '20210628', '20210629', '20210630', '20210701', '20210702', '20210703', '20210704', '20210705', '20210706', '20210707', '20210709', '20210710', '20210711', '20210712', '20210713', '20210714', '20210715', '20210716', '20210717', '20210718', '20210719', '20210720', '20210721', '20210722', '20210723', '20210724', '20210725', '20210726', '20210727', '20210728', '20210729', '20210730', '20210801', '20210802', '20210803', '20210804', '20210805', '20210806', '20210807', '20210808', '20210809', '20210810', '20210811', '20210813', '20210814', '20210815', '20210816', '20210817', '20210818', '20210819', '20210820', '20210821', '20210822', '20210823', '20210824', '20210826', '20210827', '20210828', '20210829', '20210830', '20210901', '20210902', '20210903', '20210904', '20210905', '20210906', '20210907', '20210908', '20210909', '20210910', '20210911', '20210912', '20210913', '20210914', '20210915', '20210916', '20210917', '20210918', '20210919', '20210920', '20210921', '20210922', '20210923', '20210924', '20210925', '20210926', '20210927', '20210928', '20210929', '20211001', '20211002', '20211003', '20211004', '20211005', '20211006', '20211007', '20211008', '20211009', '20211010', '20211011', '20211012', '20211013', '20211014', '20211015', '20211016', '20211017', '20211018', '20211019', '20211020', '20211021', '20211022', '20211023', '20211024', '20211025', '20211026', '20211027', '20211028']
nodeList=['舟山', '贵阳', '黄石', '昭通', '焦作', '南通', '丽水', '晋城', '巴中', '阜新', '合肥', '威海', '宿州', '德阳', '白山', '延安', '攀枝花', '佛山', '亳州', '天门', '濮阳', '池州', '漯河', '盐城', '厦门', '丹东', '保山', '贵港', '南昌', '绵阳', '黄冈', '廊坊', '鄂州', '渭南', '宣城', '乐山', '昆明', '淮安', '云浮', '南京', '长治', '防城港', '鞍山', '泸州', '大连', '阳泉', '盘锦', '温州', '赣州', '荆门', '西宁', '湘西土家族苗族自治州', '吉安', '开封', '铜陵', '孝感', '呼和浩特', '佳木斯', '枣庄', '眉山', '遂宁', '武汉', '许昌', '达州', '青岛', '承德', '咸阳', '驻马店', '天水', '苏州', '长春', '黑河', '连云港', '红河哈尼族彝族自治州', '辽阳', '六安', '菏泽', '衡水', '营口', '兴安盟', '岳阳', '黔南布依族苗族自治州', '湘潭', '泉州', '齐齐哈尔', '平顶山', '武威', '宜昌', '滁州', '江门', '临沧', '玉溪', '郴州', '葫芦岛', '沈阳', '商丘', '潜江', '南充', '嘉兴', '东莞', '广安', '恩施土家族苗族自治州', '乌兰察布', '潍坊', '襄阳', '天津', '茂名', '大庆', '邢台', '镇江', '张掖', '河源', '东营', '绥化', '马鞍山', '台州', '抚顺', '柳州', '西双版纳傣族自治州', '西安', '白银', '蚌埠', '揭阳', '宜春', '九江', '邵阳', '阜阳', '四平', '张家口', '湛江', '铁岭', '德宏傣族景颇族自治州', '普洱', '荆州', '伊春', '济宁', '烟台', '珠海', '太原', '本溪', '惠州', '无锡', '双鸭山', '安阳', '运城', '衡阳', '广州', '玉林', '淮北', '凉山彝族自治州', '自贡', '常德', '海南藏族自治州', '长沙', '宁德', '呼伦贝尔', '百色', '新乡', '包头', '甘孜藏族自治州', '朔州', '辽源', '海西蒙古族藏族自治州', '张家界', '重庆', '庆阳', '聊城', '泰州', '上饶', '曲靖', '郑州', '中山', '安顺', '白城', '漳州', '淮南', '桂林', '南宁', '益阳', '济源', '文山壮族苗族自治州', '北海', '抚州', '阳江', '秦皇岛', '梅州', '成都', '德州', '锦州', '安康', '巴彦淖尔', '河池', '汕头', '通化', '龙岩', '梧州', '宜宾', '莆田', '济南', '安庆', '萍乡', '深圳', '日照', '赤峰', '宁波', '平凉', '邯郸', '丽江', '大同', '汕尾', '株洲', '宿迁', '怀化', '钦州', '哈尔滨', '南平', '宝鸡', '鹤岗', '榆林', '通辽', '随州', '泰安', '鹤壁', '朝阳', '资阳', '雅安', '仙桃', '信阳', '楚雄彝族自治州', '潮州', '绍兴', '周口', '常州', '吕梁', '忻州', '景德镇', '三明', '鹰潭', '杭州', '金华', '鄂尔多斯', '衢州', '牡丹江', '陇南', '铜川', '扬州', '临夏回族自治州', '阿坝藏族羌族自治州', '芜湖', '清远', '来宾', '石家庄', '定西', '福州', '黔东南苗族侗族自治州', '广元', '洛阳', '淄博', '临汾', '娄底', '鸡西', '北京', '沧州', '崇左', '海北藏族自治州', '贺州', '湖州', '三门峡', '临沂', '肇庆', '大理白族自治州', '咸宁', '徐州', '内江', '兰州', '唐山', '永州', '黔西南布依族苗族自治州', '韶关', '晋中', '遵义', '松原', '上海', '十堰', '乌海', '金昌', '商洛', '南阳', '六盘水', '汉中', '延边朝鲜族自治州', '锡林郭勒盟', '保定', '新余', '滨州']

listXData = ['20200101', '20200102', '20200103', '20200104', '20200105', '20200106', '20200107', '20200108', '20200109', '20200110', '20200111', '20200112', '20200113', '20200114', '20200115', '20200116', '20200117', '20200118', '20200119', '20200120', '20200121', '20200122', '20200123', '20200124', '20200125', '20200126', '20200127', '20200128', '20200129', '20200130', '20200131', '20200201', '20200202', '20200203', '20200204', '20200205', '20200206', '20200207', '20200208', '20200209', '20200210', '20200211', '20200212', '20200213', '20200214', '20200215', '20200216', '20200217', '20200218', '20200219', '20200220', '20200221', '20200222', '20200223', '20200224', '20200225', '20200226', '20200227', '20200228', '20200229', '20200301', '20200302', '20200303', '20200304', '20200305', '20200306', '20200307', '20200308', '20200309', '20200310', '20200311', '20200312', '20200313', '20200314', '20200315', '20200316', '20200317', '20200318', '20200319', '20200320', '20200321', '20200322', '20200323', '20200324', '20200325', '20200326', '20200327', '20200328', '20200329', '20200330', '20200331', '20200401', '20200402', '20200403', '20200404', '20200405', '20200406', '20200407', '20200408', '20200409', '20200410', '20200411', '20200412', '20200413', '20200414', '20200415', '20200416', '20200417', '20200418', '20200419', '20200420', '20200421', '20200422', '20200423', '20200424', '20200425', '20200426', '20200427', '20200428', '20200429', '20200430', '20200501', '20200502', '20200503']

fileNamePath = "F:\\01大连民族\\百度迁徙爬取和数据\\百度迁徙数据-final\\03将两个In和Out相同行合并_最终数据\\"


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

# 计算平均最短路径长度
def averageShortestPathLength():
    """
    返回绘制图表的
    X轴：日期
    Y轴：平均平均最短路径长度
    """
    listAverageShortestPathLength = []
    listAverageShortestPathLength_superNode = []
    for i in range(len(listXData)):
        # 循环画图
        try:
            filePathInMethon = fileNamePath + listXData[i] + "finalData.csv"
            print(filePathInMethon)
            G = drawpicture(filePathInMethon)
            for city_want in nodeList:
                G.add_edges_from([(city_want, "超级节点")])
        except Exception as problem:
            print("((平均最短路径长度) error打开迁徙文件出问题：", problem)
        else:
            # AEC_LastValue =0
            # for C in (G.subgraph(c).copy() for c in nx.connected_components(G)):
            #     AEC_LastValue = AEC_LastValue + nx.average_shortest_path_length(C)
            # listAverageShortestPathLength.append(AEC_LastValue)
            listAverageShortestPathLength_superNode.append(nx.average_shortest_path_length(G))
    print("(平均最短路径长度)X轴数值： ", listXData)
    print("(平均最短路径长度)Y轴数值： ", listAverageShortestPathLength_superNode)

    # 画图 设置X轴显示效果
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # 为了设置x轴时间的显示
    def format_fn(tick_val, tick_pos):
        if int(tick_val) in range(len(listXData)):
            return listXData[int(tick_val)]
        else:
            return ''
    ax.xaxis.set_major_formatter(FuncFormatter(format_fn))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # plt.ylim((-5, 40))
    # 横坐标每个值旋转90度
    # plt.xticks(rotation=90)
    # 设置Mac上的字体
    # font = FontProperties(fname='/Library/Fonts/Arial Unicode.ttf')
    font = matplotlib.font_manager.FontProperties(
        fname='C:\\Windows\\Fonts\\SimHei.ttf')
    # 坐标轴ticks的字体大小
    plt.tick_params(labelsize=5)
    plt.yticks(fontsize=10)
    plt.xticks(fontsize=7)
    plt.xlabel('日期', FontProperties=font)
    plt.ylabel('平均最短路径长度', FontProperties=font)
    plt.title('百度迁徙2020上半年平均最短路径长度折线图', FontProperties=font)
    ax.plot(listXData, listAverageShortestPathLength,"m.-", linewidth=1, color='blue')
    plt.show()


# 直接调用函数画图
averageShortestPathLength()
# 最新的结果
# (平均最短路径长度)Y轴数值：  [8.43676991021029, 7.828100021114229, 3.7799517555615116, 3.774075687185443, 3.619136870434448, 3.61774099883856, 3.710462640340689, 3.540819783197832, 3.524946767324816, 3.7680612070855974, 3.6780391018195897, 3.8791330257593235, 3.698364305071622, 3.9012291908633374, 3.8956409444214324, 4.993828696560991, 5.044933964864797, 5.033444483153337, 5.201162819838108, 5.203180212014134, 5.03807758833704, 5.271435631331851, 5.837831741974288, 12.480083250384581, 35.24476044926376, 16.651609260304912, 20.898821595436328, 24.907870052300392, 39.757369371921605, 41.467871017871026, 45.78059856809857, 46.47159692159692, 43.44917455511968, 45.435150375939855, 46.29118071471013, 44.80913122824888, 40.61895212630506, 39.47722604193193, 38.37095959595959, 44.586796536796534, 43.73030303030303, 43.436868686868685, 41.949000999001, 45.52611832611833, 46.52784992784993, 45.273737373737376, 45.38492063492064, 48.36115502854633, 50.160154338415204, 46.92138378862517, 46.04711144590178, 45.96940836940837, 45.25208269553682, 45.060224337066444, 38.41647117699597, 38.06930551514818, 36.693763883468264, 34.69409146364322, 35.71241530275541, 33.05249158860978, 32.77481865660458, 33.731304850305875, 31.803559477425175, 30.978582414121675, 32.00601990178649, 31.538173637950553, 29.337975372380562, 32.042030273170624, 30.923700673464126, 29.995444264806224, 29.496218765584963, 28.44474189505201, 25.11603747821499, 24.227367822882492, 23.375576753098603, 22.218470431058158, 24.162873235614722, 24.41036592736164, 26.381459984293567, 21.697830992536876, 16.291898634453784, 18.76912720004442, 18.814267595237485, 19.343662820593032, 16.266809106911246, 16.687503952444192, 19.0468470304734, 17.86547821799488, 15.877886441541598, 15.79940738080273, 13.006997600101048, 16.486466165413532, 20.835750633191022, 18.74434322695501, 14.278786485865318, 13.596519174041298, 18.0383375415021, 19.73157118472079, 19.725685082386114, 37.45724146120962, 20.206431273644387, 13.653932920094084, 12.712676246373878, 12.221847389558233, 12.056230296996848, 12.113951154232184, 12.022917363666778, 11.95699251163732, 13.604825193675797, 13.018561855121796, 13.148761764119874, 13.454787956804692, 13.590202120245038, 18.608992973357115, 13.229177747048187, 13.25904555836038, 13.857466371256173, 15.056100110282621, 12.073034987878277, 13.545237546568346, 12.61810558414332, 6.39592290585619, 8.56168709119615, 9.593489211337493]

averageShortestPathLength_superNode =  [2.0002244618527083, 2.001436555857332, 1.9963188256155866, 1.994119099459047, 1.9949047159435254, 1.9960943637628785, 1.9960943637628785, 1.9948822697582547, 1.9938272990505264, 1.9951291777962334, 1.9942762227559425, 1.9956229938721914, 1.9956229938721914, 1.9964535027272114, 1.9965432874682947, 1.9968350878768153, 1.9970146573589818, 1.9958923480954411, 1.9966555183946488, 1.996049471392337, 1.99447823842338, 1.9958923480954411, 1.9975309196202105, 1.9999326614441875, 2.0027159884177683, 1.9986083365132097, 2.0006509393728535, 2.003726066754955, 2.0060604700231197, 2.00662162465489, 2.007788826288972, 2.0084397656618256, 2.0076765953626183, 2.00911315121995, 2.003502587395205, 2.00366076876144, 2.003864144803742, 2.004067520846044, 2.0039545341558767, 2.004044923508011, 2.003818950127675, 2.004180507536212, 2.004406480916548, 2.00429349422638, 2.010931292226886, 2.004406480916548, 2.010976184597428, 2.0097865367780745, 2.0096967520369913, 2.009606967295908, 2.0030732379725666, 2.0023275258174587, 2.007564364436264, 2.0072276716572017, 2.0058809005409532, 2.0058584543556823, 2.0058360081704114, 2.0059033467262237, 2.005185068797558, 2.004332113757267, 2.004758591277412, 2.004803483647954, 1.998440783675683, 1.9984859783517501, 1.9979210449009106, 1.9976498768445077, 1.9971753327458026, 2.004197436645642, 1.9971301380697355, 1.9972431247599032, 2.003456712531705, 2.0031873583084554, 2.0027159884177683, 2.0015936791542277, 2.0019977104891025, 2.0015936791542277, 2.002177279971269, 2.0021099414154566, 2.002042602859644, 2.0014814482278735, 2.000044892370542, 2.000987632151916, 2.0003142465937915, 2.000965185966645, 2.000718277928666, 2.001212094004624, 2.000852955040291, 2.000448923705416, 1.999977553814729, 1.9998877690736458, 2.000112230926354, 1.9827989005955107, 1.983394411360513, 1.9823179111314704, 1.9875557375557376, 1.9876012376012375, 1.9897169897169897, 1.98996723996724, 1.9905814905814905, 1.9931977431977432, 1.991036491036491, 1.9886477386477386, 1.9883519883519885, 1.9875784875784877, 1.9882154882154883, 1.9882609882609883, 1.9882382382382382, 1.988078988078988, 1.9885339885339886, 1.987851487851488, 1.9877604877604877, 1.9884657384657385, 1.9888752388752389, 1.9901264901264901, 1.9881699881699881, 1.988056238056238, 2.012890365448505, 2.0130232558139536, 2.011827242524917, 2.0124695459579183, 2.011827242524917, 2.005337763012182, 2.0083499446290145, 2.0077740863787374]