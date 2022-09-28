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


# file_path = "F:/封城数据处理/封城数据/石家庄/石家庄四阶/garbage_self_network/deal_01/in/"

file_path = "F:/封城数据处理/封城数据/西安/西安一阶/deal_03/"

listXData = getdaylist(20211209,20220131)




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



if __name__ == '__main__':
    averagenodeconnectivity(file_path,"西安",five_order_xian)
    get_city_degree(file_path,"西安",five_order_xian)
    edge_number(file_path,"西安",five_order_xian)
    naturecconnectivity(file_path,"西安",five_order_xian)

