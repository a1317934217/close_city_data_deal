#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 9:32
# @Author  : wuhao
# @Email   : guess?????
# @File    : deledatainfo.py
import datetime
import csv
import time

import networkx as nx
import pandas as pd
import numpy as np

# 获取时间列表
from tqdm import tqdm


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
# 最终的天数集合
# listDate_finally = ['20200101', '20200102', '20200103', '20200104', '20200105', '20200106', '20200107', '20200108', '20200109', '20200110', '20200111', '20200112', '20200113', '20200114', '20200115', '20200116', '20200117', '20200118', '20200119', '20200120', '20200121', '20200122', '20200123', '20200124', '20200125', '20200126', '20200127', '20200128', '20200129', '20200130', '20200131', '20200201', '20200202', '20200203', '20200204', '20200205', '20200206', '20200207', '20200208', '20200209', '20200210', '20200211', '20200212', '20200213', '20200214', '20200215', '20200216', '20200217', '20200218', '20200219', '20200220', '20200221', '20200222', '20200223', '20200224', '20200225', '20200226', '20200227', '20200228', '20200229', '20200301', '20200302', '20200303', '20200304', '20200305', '20200306', '20200307', '20200308', '20200309', '20200310', '20200311', '20200312', '20200313', '20200314', '20200315', '20200316', '20200317', '20200318', '20200319', '20200320', '20200321', '20200322', '20200323', '20200324', '20200325', '20200326', '20200327', '20200328', '20200329', '20200330', '20200331', '20200401', '20200402', '20200403', '20200404', '20200405', '20200406', '20200407', '20200408', '20200409', '20200410', '20200411', '20200412', '20200413', '20200414', '20200415', '20200416', '20200417', '20200418', '20200419', '20200420', '20200421', '20200422', '20200423', '20200424', '20200425', '20200426', '20200427', '20200428', '20200429', '20200430', '20200501', '20200502', '20200503', '20201001', '20201002', '20201003', '20201004', '20201005', '20201006', '20201007', '20201008', '20201009', '20201010', '20201011', '20201012', '20201013', '20201014', '20201015', '20201016', '20201017', '20201018', '20201019', '20201020', '20201021', '20201022', '20201023', '20201024', '20201025', '20201026', '20201027', '20201028', '20201029', '20201030', '20201031', '20201101', '20201102', '20201103', '20201104', '20201105', '20201106', '20201107', '20201108', '20201109', '20201110', '20201111', '20201112', '20201113', '20201114', '20201115', '20201116', '20201117', '20201118', '20201119', '20201120', '20201121', '20201122', '20201123', '20201124', '20201125', '20201126', '20201127', '20201128', '20201129', '20201130', '20201201', '20201202', '20201203', '20201204', '20201205', '20201206', '20201207', '20201208', '20201209', '20201210', '20201211', '20201212', '20201213', '20201214', '20201215', '20201216', '20201217', '20201218', '20201219', '20201220', '20201221', '20201222', '20201223', '20201224', '20201225', '20201226', '20201227', '20201228', '20201229', '20201230', '20201231', '20210101', '20210102', '20210103', '20210104', '20210105', '20210106', '20210107', '20210108', '20210109', '20210110', '20210111', '20210112', '20210113', '20210114', '20210115', '20210116', '20210117', '20210118', '20210119', '20210120', '20210121', '20210122', '20210123', '20210124', '20210125', '20210126', '20210127', '20210128', '20210129', '20210130', '20210131', '20210201', '20210202', '20210203', '20210204', '20210205', '20210206', '20210207', '20210208', '20210209', '20210210', '20210211', '20210212', '20210213', '20210214', '20210215', '20210216', '20210217', '20210218', '20210219', '20210220', '20210221', '20210222', '20210223', '20210224', '20210225', '20210226', '20210227', '20210228', '20210301', '20210302', '20210303', '20210304', '20210305', '20210306', '20210307', '20210308', '20210309', '20210310', '20210311', '20210312', '20210313', '20210314', '20210315', '20210316', '20210317', '20210318', '20210319', '20210320', '20210321', '20210322', '20210323', '20210324', '20210325', '20210326', '20210327', '20210328', '20210329', '20210330', '20210331', '20210401', '20210402', '20210403', '20210404', '20210405', '20210406', '20210407', '20210408', '20210409', '20210410', '20210411', '20210412', '20210413', '20210414', '20210415', '20210416', '20210417', '20210418', '20210419', '20210420', '20210421', '20210422', '20210423', '20210424', '20210425', '20210426', '20210427', '20210428', '20210429', '20210430', '20210501', '20210502', '20210503', '20210504', '20210505', '20210506', '20210507', '20210508', '20210509', '20210510', '20210511', '20210512', '20210513', '20210514', '20210515', '20210516', '20210517', '20210518', '20210519', '20210520', '20210521', '20210522', '20210523', '20210524', '20210525', '20210526', '20210527', '20210528', '20210529', '20210530', '20210531', '20210601', '20210602', '20210603', '20210604', '20210605', '20210606', '20210607', '20210608', '20210609', '20210610', '20210611', '20210612', '20210613', '20210614', '20210615', '20210616', '20210617', '20210618', '20210619', '20210620', '20210621', '20210622', '20210623', '20210624', '20210625', '20210626', '20210627', '20210628', '20210629', '20210630', '20210701', '20210702', '20210703', '20210704', '20210705', '20210706', '20210707', '20210709', '20210710', '20210711', '20210712', '20210713', '20210714', '20210715', '20210716', '20210717', '20210718', '20210719', '20210720', '20210721', '20210722', '20210723', '20210724', '20210725', '20210726', '20210727', '20210728', '20210729', '20210730', '20210801', '20210802', '20210803', '20210804', '20210805', '20210806', '20210807', '20210808', '20210809', '20210810', '20210811', '20210813', '20210814', '20210815', '20210816', '20210817', '20210818', '20210819', '20210820', '20210821', '20210822', '20210823', '20210824', '20210826', '20210827', '20210828', '20210829', '20210830', '20210901', '20210902', '20210903', '20210904', '20210905', '20210906', '20210907', '20210908', '20210909', '20210910', '20210911', '20210912', '20210913', '20210914', '20210915', '20210916', '20210917', '20210918', '20210919', '20210920', '20210921', '20210922', '20210923', '20210924', '20210925', '20210926', '20210927', '20210928', '20210929', '20211001', '20211002', '20211003', '20211004', '20211005', '20211006', '20211007', '20211008', '20211009', '20211010', '20211011', '20211012', '20211013', '20211014', '20211015', '20211016', '20211017', '20211018', '20211019', '20211020', '20211021', '20211022', '20211023', '20211024', '20211025', '20211026', '20211027', '20211028']
listDate_finally = getdaylist(20201001,20220508)

# 最终的路径
fileNamePath_finally = "F:\\01大连民族\\百度迁徙爬取和数据\\百度迁徙数据-final\\03将两个In和Out相同行合并_最终数据\\"

fileName = "F:\\01大连民族\\百度迁徙爬取和数据\\百度迁徙数据-final\\"
# 需要留下的节点
lastname = {'威海', '三门峡', '白沙黎族自治县', '攀枝花', '陵水黎族自治县', '通辽', '桂林', '汕头', '枣庄', '绵阳', '达州', '阜阳', '普洱', '榆林', '齐齐哈尔', '衢州', '邢台', '嘉峪关', '益阳', '商丘', '天水', '恩施土家族苗族自治州', '云浮', '哈密', '德宏傣族景颇族自治州', '昌江黎族自治县', '白城', '秦皇岛', '铁岭', '四平', '咸阳', '平凉', '佳木斯', '万宁', '广州', '陇南', '临夏回族自治州', '昭通', '南通', '本溪', '开封', '青岛', '玉溪', '三亚', '哈尔滨', '三明', '阜新', '衡水', '西宁', '淮南', '来宾', '东莞', '保定', '承德', '马鞍山', '安康', '佛山', '白山', '百色', '丽水', '延边朝鲜族自治州', '沧州', '东营', '邵阳', '遵义', '赣州', '驻马店', '凉山彝族自治州', '中山', '菏泽', '襄樊', '泰州', '北海', '崇左', '兰州', '芜湖', '思茅', '白银', '临高县', '中卫', '文山壮族苗族自治州', '绥化', '焦作', '钦州', '六盘水', '荆门', '张掖', '楚雄彝族自治州', '大理白族自治州', '大庆', '吴忠', '柳州', '池州', '福州', '常州', '玉林', '黔东南苗族侗族自治州', '澳门', '东方', '安阳', '抚顺', '黄冈', '南充', '苏州', '黄石', '香港', '泰安', '长春', '景德镇', '龙岩', '阳江', '湘潭', '河池', '庆阳', '宜春', '张家口', '贺州', '揭阳', '潍坊', '黄南藏族自治州', '拉萨', '铜川', '宣城', '平顶山', '德州', '常德', '锡林郭勒盟', '防城港', '昆明', '琼海', '兴安盟', '渭南', '文昌', '阳泉', '鹤壁', '襄阳', '和田地区', '淮安', '咸宁', '南宁', '海东', '乌海', '广安', '呼和浩特', '安顺', '遂宁', '蚌埠', '黑河', '潜江', '天门', '重庆', '大同', '镇江', '武汉', '黄山', '鹤岗', '江门', '营口', '海口', '岳阳', '澄迈县', '巴音郭楞蒙古自治州', '廊坊', '临沂', '乌兰察布', '无锡', '吕梁', '黔南布依族苗族自治州', '定西', '怀化', '株洲', '九江', '南昌', '延安', '阿拉善盟', '贵港', '绍兴', '忻州', '商洛', '长治', '韶关', '宿州', '烟台', '巴中', '梧州', '松原', '太原', '随州', '南平', '乌鲁木齐', '郑州', '喀什地区', '博尔塔拉蒙古自治州', '聊城', '唐山', '酒泉', '海西蒙古族藏族自治州', '丹东', '朝阳', '昆玉', '濮阳', '神农架林区', '儋州', '衡阳', '果洛藏族自治州', '滁州', '辽源', '曲靖', '贵阳', '抚州', '琼中黎族苗族自治县', '萍乡', '银川', '牡丹江', '周口', '成都', '金昌', '湖州', '宿迁', '鹰潭', '朔州', '徐州', '六安', '乐东黎族自治县', '许昌', '包头', '通化', '漯河', '南阳', '肇庆', '迪庆藏族自治州', '清远', '吉林', '赤峰', '孝感', '武威', '吉安', '毕节', '新乡', '晋城', '日照', '长沙', '仙桃', '淮北', '鄂尔多斯', '淄博', '荆州', '汕尾', '安庆', '杭州', '德阳', '大兴安岭地区', '宜昌', '眉山', '阿坝藏族羌族自治州', '厦门', '合肥', '沈阳', '伊犁哈萨克自治州', '娄底', '巴彦淖尔', '温州', '上海', '西安', '雅安', '天津', '图木舒克', '阿克苏地区', '运城', '连云港', '潮州', '金华', '乐山', '晋中', '永州', '济南', '扬州', '锦州', '宝鸡', '临汾', '宁德', '河源', '北京', '珠海', '漳州', '深圳', '南京', '亳州', '大连', '湘西土家族苗族自治州', '甘孜藏族自治州', '鞍山', '呼伦贝尔', '信阳', '红河哈尼族彝族自治州', '汉中', '石嘴山', '惠州', '滨州', '七台河', '梅州', '洛阳', '辽阳', '丽江', '十堰', '湛江', '泉州', '石家庄', '黔西南布依族苗族自治州', '宁波', '盐城', '玉树藏族自治州', '嘉兴', '台州', '泸州', '铜仁', '茂名', '伊春', '定安县', '葫芦岛', '资阳', '济源', '邯郸', '甘南藏族自治州', '广元', '上饶', '郴州', '盘锦', '济宁'}
def as_num(x):
    y = '{:.10f}'.format(x)  # .10f 保留10位小数
    return float(y)
#0.055  295个城市  删除87个城市
# deal_city = ['林芝地区', '图木舒克', '阿里地区', '海西蒙古族藏族自治州', '克孜勒苏柯尔克孜自治州', '陇南', '喀什地区', '塔城地区', '五指山', '乐东黎族自治县', '临夏回族自治州', '七台河', '甘南藏族自治州', '那曲地区', '果洛藏族自治州', '海南藏族自治州', '山南地区', '陵水黎族自治县', '可克达拉', '阿克苏地区', '石河子', '广西壮族自治区', '昆玉', '琼海', '白银', '北屯', '万宁', '海东地区', '酒泉', '宁夏回族自治区', '金昌', '临高', '五家渠', '伊春', '阿勒泰地区', '鸡西', '玉树藏族自治州', '天水', '内蒙古自治区', '张掖', '昌都地区', '伊犁哈萨克自治州', '东方', '定安', '保亭黎族苗族自治县', '新疆维吾尔自治区', '昌吉回族自治州', '阿拉尔', '西藏自治区', '昌江黎族自治县', '武威', '白山', '临沧', '儋州', '巴音郭楞蒙古自治州', '西宁', '文昌', '思茅', '日喀则地区', '毕节', '襄樊', '嘉峪关', '吐鲁番地区', '黄南藏族自治州', '铜仁地区', '平凉', '神农架林区', '博尔塔拉蒙古自治州', '铜仁', '定西', '克拉玛依', '哈密地区', '海北藏族自治州', '三亚', '怒江傈僳族自治州', '屯昌', '双河', '铁门关', '澳门', '澄迈', '浙江', '和田地区', '琼中黎族苗族自治县', '白沙黎族自治县', '莱芜', '毕节地区', '大兴安岭地区']

print(len(lastname))
# 需要删除的节点 这里用的0.04阈值
delcityName = ['双鸭山','海南藏族自治州','海北藏族自治州','澳门', '克拉玛依', '白沙黎族自治县', '文昌', '东方', '吴忠', '和田地区', '黄南藏族自治州', '迪庆藏族自治州', '昌江黎族自治县', '乌鲁木齐', '陵水黎族自治县', '阿克苏地区', '保亭黎族苗族自治县', '北屯', '伊犁哈萨克自治州', '五指山', '阿拉善盟', '浙江', '林芝地区', '儋州', '阿拉尔', '吐鲁番地区', '昌都地区', '定安', '克孜勒苏柯尔克孜自治州', '日喀则地区', '哈密地区', '莱芜', '果洛藏族自治州', '山南地区', '毕节地区', '嘉峪关', '玉树藏族自治州', '阿里地区', '琼中黎族苗族自治县', '海口', '那曲地区', '固原', '铁门关', '新疆维吾尔自治区', '阿勒泰地区', '怒江傈僳族自治州', '石嘴山', '万宁', '七台河', '广西壮族自治区', '五家渠', '酒泉', '石河子', '内蒙古自治区', '宁夏回族自治区', '可克达拉', '拉萨', '琼海', '神农架林区', '图木舒克', '昆玉', '乐东黎族自治县', '西藏自治区', '甘南藏族自治州', '三亚', '双河', '昌吉回族自治州', '博尔塔拉蒙古自治州', '大兴安岭地区', '塔城地区', '中卫', '巴音郭楞蒙古自治州', '海东地区', '香港', '银川', '屯昌', '铜仁地区', '澄迈', '喀什地区', '临高', '黄山','澄迈县','临高县',"吐鲁番",'山南',"那曲","日喀则"]

print(len(delcityName))
# 需要去除某几个城市
dealdatetwo =[]

 #判断2个字符串字符是否完全一样 顺序可不同
def compare_two_str(a,b):
    if len(a) != len(b):
        return False
    return sorted(a) == sorted(b)
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

def deal_four_threshold_and_deal_city_name(beginTime,endTime):
    """
    处理删除不需要的城市和阈值小于0.04的数据
    :param beginTime:
    :param endTime:
    :return:
    """
    dayList = getdaylist(beginTime,endTime)
    for j in tqdm(range(len(dayList)),desc="第一步处理进度：",total=len(dayList)):
        # nowTimebegin = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("第一步这天开始时间为(in)：" + dayList[j])
        # 迁入数据
        field_order_move_in = ["city_name", 'city_id_name', 'num']
        # 开始写入数据
        with open(fileName + "01去掉不用的点和小于0.04阈值\\in\\" + dayList[j] + "delNodeCityFour.csv", 'w',
                  encoding="utf-8", newline='') as csvfile_in:
            writer = csv.DictWriter(csvfile_in, field_order_move_in)
            writer.writeheader()
            try:
                filePathNameIn = fileName+"in\\"+dayList[j]+".csv"
                dataWantdelColIn = pd.read_csv(filePathNameIn)
            except Exception as problem:
                print("error打开physical本地数据有问题：", problem)
            else:
                for cityNameIn_i in dataWantdelColIn.iterrows():
                    if cityNameIn_i[1]["city_name"] not in delcityName and cityNameIn_i[1]["city_id_name"] not in delcityName and float(cityNameIn_i[1]["num"]) > 0.04:
                        row = {"city_name": cityNameIn_i[1]["city_name"], "city_id_name": cityNameIn_i[1]["city_id_name"], "num": cityNameIn_i[1]["num"]}
                        writer.writerow(row)

        # 迁出数据
        # 开始写入数据
        with open(fileName + "01去掉不用的点和小于0.04阈值\\out\\" + dayList[j] + "delNodeCityFour.csv", 'w',
                  encoding="utf-8", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, field_order_move_in)
            writer.writeheader()
            print("第一步这天开始时间为(out)：" + dayList[j])
            try:
                filePathNameOut = fileName + "out\\" + dayList[j] + ".csv"
                dataWantdelColOut = pd.read_csv(filePathNameOut)
            except Exception as problem:
                print("error打开physical本地数据有问题：", problem)
            else:
                # 定位问题处理
                # pointer=1
                for cityName_Out in dataWantdelColOut.iterrows():
                    # print(pointer)
                    # pointer+=1
                    if cityName_Out[1]["city_name"] not in delcityName and cityName_Out[1]["city_id_name"] not in delcityName and  float(cityName_Out[1]["num"]) > 0.04:
                        row = {"city_name": cityName_Out[1]["city_name"], "city_id_name": cityName_Out[1]["city_id_name"], "num": cityName_Out[1]["num"]}
                        writer.writerow(row)
        # nowTimeEnd = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # print("第一步：：" + dayList[j], "这天结束时间为", nowTimeEnd)
def deal_sameCol_in_Alonecsv(beginTime,endTime):
    """
    处理单独的in或out的数据重复问题
    :param beginTime:
    :param endTime:
    :return:
    """
    dayList = getdaylist(beginTime, endTime)

    # 循环取每一天的值
    for i in tqdm(range(len(dayList)),desc="第二步处理进度：",total=len(dayList)):
        # nowTimebegin = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("第二步这天开始时间为（in）：" + dayList[i])
        # 创建处理完的数据csv
        # 表头
        field_order_move_in = ["city_name", 'city_id_name', 'num']
        # 迁入数据
        try:
            moveIn_one = pd.read_csv(fileName + "01去掉不用的点和小于0.04阈值\\in\\" + dayList[i] + "delNodeCityFour.csv")
        except Exception as problem:
            print("error打开迁出（out）有问题：", problem)
        else:
            # 开始写入整理完的数据csv
            with open(fileName + "02单独的In和out进行相同行合并\\in\\" + dayList[i] + "delNodeCityFour_Alone.csv", 'w',
                      encoding="utf-8", newline='') as csvfile_in:
                writer_in = csv.DictWriter(csvfile_in, field_order_move_in)
                writer_in.writeheader()
                # move_in 每一行
                for index_one in range(len(moveIn_one)-1):
                    every_one_row = moveIn_one.loc[index_one]
                    value_in_one = every_one_row[2]
                    compare_str_in_one =every_one_row[0]+","+every_one_row[1]
                    for row_in_two in range(index_one+1,len(moveIn_one)):
                        every_two_row = moveIn_one.loc[row_in_two]
                        value_in_two = every_two_row[2]
                        compare_str_in_two = every_two_row[1] + "," + every_two_row[0]
                        if compare_str_in_one == compare_str_in_two:
                            row = {"city_name": every_one_row[0],"city_id_name": every_one_row[1],
                                   "num": (float(value_in_one)+float(value_in_two))/2}
                            writer_in.writerow(row)
        # 迁出数据
        print("第二步这天开始时间为（out）：" + dayList[i])
        try:
            moveOut_one = pd.read_csv(fileName + "01去掉不用的点和小于0.04阈值\\out\\" + dayList[i] + "delNodeCityFour.csv")
            # moveOut_two = pd.read_csv(fileName + "01去掉不用的点和小于0.04阈值\\out\\" + dayList[i] + "delNodeCityFour.csv")
        except Exception as problem:
            print("error打开迁入（in）有问题：", problem)
        # 开始写入out数据
        else:
            with open(fileName + "02单独的In和out进行相同行合并\\out\\" + dayList[i] + "delNodeCityFour_Alone.csv", 'w',
                      encoding="utf-8", newline='') as csvfile_out:
                writer_out = csv.DictWriter(csvfile_out, field_order_move_in)
                writer_out.writeheader()
                for index_two in range(len(moveOut_one)-1):
                    every_one_row_out = moveOut_one.loc[index_two]
                    value_out_one = every_one_row_out[2]
                    compare_str_out_one = every_one_row_out[0] + "," + every_one_row_out[1]
                    for row_out_two in range(index_two+1,len(moveOut_one)):
                        every_two_row_out = moveOut_one.loc[row_out_two]
                        value_out_two = every_two_row_out[2]
                        compare_str_out_two = every_two_row_out[1] + "," + every_two_row_out[0]
                        if compare_str_out_one == compare_str_out_two:
                            row = {"city_name": every_one_row_out[0], "city_id_name": every_one_row_out[1],
                                   "num": (float(value_out_one) + float(value_out_two)) / 2}
                            writer_out.writerow(row)

            # nowTimeEnd = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # print("第二步：：" + dayList[i], "这天结束时间为", nowTimeEnd)
def merge_inAndout_final_data(beginTime,endTime):
    dayList = getdaylist(beginTime, endTime)
    # dayList = ["20200101"]
    # 循环取每一天的值
    for i in tqdm(range(len(dayList)),desc="第三步处理进度：",total=len(dayList)):
        nowTimebegin = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("第三步：："+dayList[i], "这天开始时间为", nowTimebegin)
        # 迁入数据
        try:
            moveIn = pd.read_csv(fileName + "02单独的In和out进行相同行合并\\in\\" + dayList[i] + "delNodeCityFour_Alone.csv")
        except Exception as problem:
            print("error打开迁入（in）有问题：", problem)
            continue
        # 迁出数据
        try:
            moveOut = pd.read_csv(fileName + "02单独的In和out进行相同行合并\\out\\" + dayList[i] + "delNodeCityFour_Alone.csv")
        except Exception as problem:
            print("error打开迁出（out）有问题：", problem)
            continue

        # 创建处理完的数据csv
        # 表头
        field_order_move_in = ["city_name", 'city_id_name', 'num']
        # 开始写入整理完的数据csv
        with open(fileName + "03将两个In和Out相同行合并_最终数据\\" + dayList[i] + "finalData.csv", 'w',
                  encoding="utf-8", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, field_order_move_in)
            writer.writeheader()
            # move_in 每一行
            # 提高运算效率。简化数据，指标
            for moveOut_city_i in range(moveOut["city_name"].count()):
                # 使用列表比较是否相同move_in
                listMoveOut = []
                indexColMoveOut = moveOut.loc[moveOut_city_i]
                listMoveOut.append(indexColMoveOut[0])
                listMoveOut.append(indexColMoveOut[1])
                # move_out 每一行
                for moveIn_city_j in range(moveIn["city_name"].count()):
                    # 使用列表比较是否相同move_out
                    listMoveIn = []
                    indexColMoveIn = moveIn.loc[moveIn_city_j]
                    listMoveIn.append(indexColMoveIn[0])
                    listMoveIn.append(indexColMoveIn[1])
                    # 判断两个列表是否相同 ，来进value值相加除二
                    if compare_two_str(listMoveOut, listMoveIn):
                        valueColThree = (float(indexColMoveIn[2]) + float(indexColMoveOut[2])) / 2
                        row = {"city_name": indexColMoveIn[0], "city_id_name": indexColMoveIn[1],
                               "num": valueColThree}
                        writer.writerow(row)


        nowTimeEnd = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("第三步：："+dayList[i], "这天结束时间为", nowTimeEnd)
        csvfile.close()
def deal_name_bysmall_city():
    """
    如果出现需要去除某一城市需求  则运行此文件
    :return:
    """
    for j in range(len(listDate_finally)):
        try:
            filePathNameIn = fileNamePath_finally + listDate_finally[j] + "finalData.csv"
            dataWantdelCol = pd.read_csv(filePathNameIn)
        except Exception as problem:
            print("error打开physical本地数据有问题：", problem)
        else:
            for cityNameIn_i in range(len(dataWantdelCol)):
                indexColMoveIn = dataWantdelCol.loc[cityNameIn_i]
                if indexColMoveIn[0] in dealdatetwo or indexColMoveIn[1] in dealdatetwo :
                    dataWantdelCol = dataWantdelCol.drop(cityNameIn_i)
            dataWantdelCol.to_csv(fileNamePath_finally +"\\latdata\\" + listDate_finally[j] + "finalData.csv", index=False, encoding="utf-8-sig")

#
#
# (20210101,20210101)
deal_four_threshold_and_deal_city_name(20220509,20220620)

#
deal_sameCol_in_Alonecsv(20220509,20220620)

# #
merge_inAndout_final_data(20220509,20220620)


# deal_name_bysmall_city()

