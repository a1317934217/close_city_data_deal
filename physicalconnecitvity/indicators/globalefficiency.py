#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 16:11
# @Author  : wuhao
# @Email   : guess?????
# @File    : globalefficiency.py
# 全局效率

import datetime

import matplotlib
import networkx as nx
import numpy as np
import pandas as pd
# coding=utf-8
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import FuncFormatter, MaxNLocator
# 根据路径画图
from numpy import array
# listXData = ['20200101', '20200102', '20200103', '20200104', '20200105', '20200106', '20200107', '20200108', '20200109', '20200110', '20200111', '20200112', '20200113', '20200114', '20200115', '20200116', '20200117', '20200118', '20200119', '20200120', '20200121', '20200122', '20200123', '20200124', '20200125', '20200126', '20200127', '20200128', '20200129', '20200130', '20200131', '20200201', '20200202', '20200203', '20200204', '20200205', '20200206', '20200207', '20200208', '20200209', '20200210', '20200211', '20200212', '20200213', '20200214', '20200215', '20200216', '20200217', '20200218', '20200219', '20200220', '20200221', '20200222', '20200223', '20200224', '20200225', '20200226', '20200227', '20200228', '20200229', '20200301', '20200302', '20200303', '20200304', '20200305', '20200306', '20200307', '20200308', '20200309', '20200310', '20200311', '20200312', '20200313', '20200314', '20200315', '20200316', '20200317', '20200318', '20200319', '20200320', '20200321', '20200322', '20200323', '20200324', '20200325', '20200326', '20200327', '20200328', '20200329', '20200330', '20200331', '20200401', '20200402', '20200403', '20200404', '20200405', '20200406', '20200407', '20200408', '20200409', '20200410', '20200411', '20200412', '20200413', '20200414', '20200415', '20200416', '20200417', '20200418', '20200419', '20200420', '20200421', '20200422', '20200423', '20200424', '20200425', '20200426', '20200427', '20200428', '20200429', '20200430', '20200501', '20200502', '20200503', '20201001', '20201002', '20201003', '20201004', '20201005', '20201006', '20201007', '20201008', '20201009', '20201010', '20201011', '20201012', '20201013', '20201014', '20201015', '20201016', '20201017', '20201018', '20201019', '20201020', '20201021', '20201022', '20201023', '20201024', '20201025', '20201026', '20201027', '20201028', '20201029', '20201030', '20201031', '20201101', '20201102', '20201103', '20201104', '20201105', '20201106', '20201107', '20201108', '20201109', '20201110', '20201111', '20201112', '20201113', '20201114', '20201115', '20201116', '20201117', '20201118', '20201119', '20201120', '20201121', '20201122', '20201123', '20201124', '20201125', '20201126', '20201127', '20201128', '20201129', '20201130', '20201201', '20201202', '20201203', '20201204', '20201205', '20201206', '20201207', '20201208', '20201209', '20201210', '20201211', '20201212', '20201213', '20201214', '20201215', '20201216', '20201217', '20201218', '20201219', '20201220', '20201221', '20201222', '20201223', '20201224', '20201225', '20201226', '20201227', '20201228', '20201229', '20201230', '20201231', '20210101', '20210102', '20210103', '20210104', '20210105', '20210106', '20210107', '20210108', '20210109', '20210110', '20210111', '20210112', '20210113', '20210114', '20210115', '20210116', '20210117', '20210118', '20210119', '20210120', '20210121', '20210122', '20210123', '20210124', '20210125', '20210126', '20210127', '20210128', '20210129', '20210130', '20210131', '20210201', '20210202', '20210203', '20210204', '20210205', '20210206', '20210207', '20210208', '20210209', '20210210', '20210211', '20210212', '20210213', '20210214', '20210215', '20210216', '20210217', '20210218', '20210219', '20210220', '20210221', '20210222', '20210223', '20210224', '20210225', '20210226', '20210227', '20210228', '20210301', '20210302', '20210303', '20210304', '20210305', '20210306', '20210307', '20210308', '20210309', '20210310', '20210311', '20210312', '20210313', '20210314', '20210315', '20210316', '20210317', '20210318', '20210319', '20210320', '20210321', '20210322', '20210323', '20210324', '20210325', '20210326', '20210327', '20210328', '20210329', '20210330', '20210331', '20210401', '20210402', '20210403', '20210404', '20210405', '20210406', '20210407', '20210408', '20210409', '20210410', '20210411', '20210412', '20210413', '20210414', '20210415', '20210416', '20210417', '20210418', '20210419', '20210420', '20210421', '20210422', '20210423', '20210424', '20210425', '20210426', '20210427', '20210428', '20210429', '20210430', '20210501', '20210502', '20210503', '20210504', '20210505', '20210506', '20210507', '20210508', '20210509', '20210510', '20210511', '20210512', '20210513', '20210514', '20210515', '20210516', '20210517', '20210518', '20210519', '20210520', '20210521', '20210522', '20210523', '20210524', '20210525', '20210526', '20210527', '20210528', '20210529', '20210530', '20210531', '20210601', '20210602', '20210603', '20210604', '20210605', '20210606', '20210607', '20210608', '20210609', '20210610', '20210611', '20210612', '20210613', '20210614', '20210615', '20210616', '20210617', '20210618', '20210619', '20210620', '20210621', '20210622', '20210623', '20210624', '20210625', '20210626', '20210627', '20210628', '20210629', '20210630', '20210701', '20210702', '20210703', '20210704', '20210705', '20210706', '20210707', '20210709', '20210710', '20210711', '20210712', '20210713', '20210714', '20210715', '20210716', '20210717', '20210718', '20210719', '20210720', '20210721', '20210722', '20210723', '20210724', '20210725', '20210726', '20210727', '20210728', '20210729', '20210730', '20210801', '20210802', '20210803', '20210804', '20210805', '20210806', '20210807', '20210808', '20210809', '20210810', '20210811', '20210813', '20210814', '20210815', '20210816', '20210817', '20210818', '20210819', '20210820', '20210821', '20210822', '20210823', '20210824', '20210826', '20210827', '20210828', '20210829', '20210830', '20210901', '20210902', '20210903', '20210904', '20210905', '20210906', '20210907', '20210908', '20210909', '20210910', '20210911', '20210912', '20210913', '20210914', '20210915', '20210916', '20210917', '20210918', '20210919', '20210920', '20210921', '20210922', '20210923', '20210924', '20210925', '20210926', '20210927', '20210928', '20210929', '20211001', '20211002', '20211003', '20211004', '20211005', '20211006', '20211007', '20211008', '20211009', '20211010', '20211011', '20211012', '20211013', '20211014', '20211015', '20211016', '20211017', '20211018', '20211019', '20211020', '20211021', '20211022', '20211023', '20211024', '20211025', '20211026', '20211027', '20211028']

listXData = ['20200101', '20200102', '20200103', '20200104', '20200105', '20200106', '20200107', '20200108', '20200109', '20200110', '20200111', '20200112', '20200113', '20200114', '20200115', '20200116', '20200117', '20200118', '20200119', '20200120', '20200121', '20200122', '20200123', '20200124', '20200125', '20200126', '20200127', '20200128', '20200129', '20200130', '20200131', '20200201', '20200202', '20200203', '20200204', '20200205', '20200206', '20200207', '20200208', '20200209', '20200210', '20200211', '20200212', '20200213', '20200214', '20200215', '20200216', '20200217', '20200218', '20200219', '20200220', '20200221', '20200222', '20200223', '20200224', '20200225', '20200226', '20200227', '20200228', '20200229', '20200301', '20200302', '20200303', '20200304', '20200305', '20200306', '20200307', '20200308', '20200309', '20200310', '20200311', '20200312', '20200313', '20200314', '20200315', '20200316', '20200317', '20200318', '20200319', '20200320', '20200321', '20200322', '20200323', '20200324', '20200325', '20200326', '20200327', '20200328', '20200329', '20200330', '20200331', '20200401', '20200402', '20200403', '20200404', '20200405', '20200406', '20200407', '20200408', '20200409', '20200410', '20200411', '20200412', '20200413', '20200414', '20200415', '20200416', '20200417', '20200418', '20200419', '20200420', '20200421', '20200422', '20200423', '20200424', '20200425', '20200426', '20200427', '20200428', '20200429', '20200430', '20200501', '20200502', '20200503']

fileNamePath = "F:\\01大连民族\\百度迁徙爬取和数据\\百度迁徙数据-final\\03将两个In和Out相同行合并_最终数据\\"

# 多重边无向图
# coding=utf-8
# 多重边无向图
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

# 计算全局效率
def globalefficiency():
    """
    返回绘制图表的
    X轴：日期
    Y轴：全局效率
    """
    # Y轴数值
    listGlobalEfficiency = []

    for i in range(len(listXData)):
        # 循环画图
        try:
            filePathInMethon = fileNamePath + listXData[i] + "finalData.csv"
            print(filePathInMethon)
            G = drawpicture(filePathInMethon)
        except Exception as problem:
            print("(全局效率) error打开迁徙文件出问题：", problem)
        else:
            listGlobalEfficiency.append(nx.global_efficiency(G))
    print( "这天的全局效率性列表为：", listGlobalEfficiency)









    # 画图 设置X轴显示效果
    fig = plt.figure(figsize=(12,6))
    ax = fig.add_subplot(111)
    # 为了设置x轴时间的显示
    def format_fn(tick_val, tick_pos):
        if int(tick_val) in range(len(listXData)):
            return listXData[int(tick_val)]
        else:
            return ''

    #
    ax.xaxis.set_major_formatter(FuncFormatter(format_fn))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # plt.ylim((-5, 40))
    # 横坐标每个值旋转90度
    # plt.xticks(rotation=90)

    # 设置Mac上的字体（Mac上跑数据的时候）
    font = matplotlib.font_manager.FontProperties(
        fname='C:\\Windows\\Fonts\\SimHei.ttf')
    # win（大壳子上跑数据的字体）
    # font = FontProperties(='C:\\Windows\\WinSxS\\amd64_microsoft-windows-font-truetype-arial_31bf3856ad364e35_10.0.19041.1_none_28747db34cb89a67\\arial.ttf')
    # 坐标轴ticks的字体大小

    plt.tick_params(labelsize=5)
    plt.yticks(fontsize=10)
    plt.xticks(fontsize=7,rotation=70,ha='right')
    plt.xlabel('日期', FontProperties=font)
    plt.ylabel('全局效率', FontProperties=font)
    plt.title('百度迁徙2020上半年全局效率折线图', FontProperties=font)
    plt.plot(listXData, listGlobalEfficiency, "m.-", linewidth=1, color='blue',label='线条')

    plt.legend(prop=font)
    plt.show()


# 调用计算
globalefficiency()
# 最新一次的跑出结果
# 这天的全局效率性列表为： [0.22598867485050303, 0.2535595386719805, 0.2951215451216049, 0.2973173957930734, 0.3049631780817071, 0.3032574191600879, 0.2993835322069657, 0.30934138391128113, 0.3112404192706714, 0.2964474259770993, 0.30091227209044386, 0.2892727747417864, 0.2988821426267356, 0.28713238344127584, 0.28758556580864847, 0.2799082593820348, 0.2762467004758683, 0.27756776362050506, 0.26868675013053506, 0.2683559228297336, 0.2773441618390486, 0.2647328677025872, 0.23935910429805798, 0.17988488397249355, 0.07045449472510476, 0.13359281799738795, 0.0953108862864593, 0.07671191069861179, 0.0469258917826783, 0.04546381315115123, 0.04296096375794973, 0.03468264972948836, 0.0448636415314612, 0.033895318943295547, 0.027355637657361764, 0.027950619096559444, 0.03138058324104825, 0.03199640778609177, 0.033427456382001675, 0.02573408792650911, 0.026830243547800735, 0.025042016806722668, 0.02548517310976555, 0.022974222746950015, 0.021904571504731428, 0.022385225276551284, 0.022881355932203386, 0.026355330129442495, 0.02559028443592201, 0.02962241865652544, 0.03131783340116673, 0.03280703227793182, 0.040411359278421224, 0.03989199644857323, 0.052278566385320586, 0.05235550372120591, 0.05306470319540383, 0.05560521535643034, 0.055295396699963785, 0.060441277387762574, 0.05600019984940896, 0.052690682275834795, 0.0575081446232631, 0.06417272592916222, 0.06141764318264525, 0.06362122271388178, 0.06396819654048166, 0.057913741423181384, 0.060015230638780864, 0.0648078770469034, 0.06583723265654522, 0.07251551069934387, 0.07640928195157966, 0.08400530188532764, 0.10138292373395397, 0.08428376277700003, 0.0814476385547203, 0.0814291523192676, 0.07520545261622551, 0.11030807843700653, 0.13162661821360913, 0.12107150878056185, 0.11633171784123249, 0.11384840148843155, 0.13040646156247637, 0.1272916634347365, 0.11717998255323005, 0.12228142717339006, 0.13499780079055737, 0.13596757780438265, 0.14380052498891066, 0.14080785624910222, 0.09221746314302041, 0.10351816366780188, 0.1459753374739022, 0.1508024487986933, 0.10198386086603621, 0.09946390964442617, 0.11889175116352017, 0.05669884993055819, 0.12043256912368393, 0.14868854453137906, 0.14758178478111392, 0.15215347349984226, 0.15335822981122046, 0.15273366637421956, 0.15373498201230307, 0.15514932126315154, 0.14778552432395103, 0.15536760358044305, 0.15311271212675223, 0.15010136328543458, 0.14863064271797483, 0.1201146682155315, 0.15229955041453155, 0.15249907447080382, 0.1435294496471538, 0.14126389065439926, 0.1521600435425559, 0.1469080903638029, 0.1553309767332616, 0.23736759131476257, 0.18313804165647646, 0.17261607531869708, 0.3172780650721993, 0.30062467294616335, 0.30240938780196114, 0.26285648121040395, 0.30786771835978805, 0.3033511698037819, 0.2878161634737629, 0.2956216221372854, 0.28867237725949196, 0.2667229852800393, 0.25397263735045483, 0.2829946041053348, 0.26602304056919535, 0.26439402792877453, 0.24374860778728993, 0.2898937633176731, 0.2881639167960582, 0.2599801188125534, 0.28960932054210065, 0.27168533885720936, 0.2670423849849857, 0.26671694559565207, 0.2818769555264595, 0.28739284126083237, 0.25810371749715116, 0.28471885434603517, 0.28006917636022033, 0.2700747555234353, 0.25744332303485423, 0.2903068858664674, 0.2854375878183964, 0.2629720988774802, 0.2768297680499919, 0.2649939533762969, 0.28215697658491157, 0.2766876179017561, 0.2756856926038274, 0.28304112966641914, 0.2366169560025431, 0.295146753155364, 0.2674156497079871, 0.26543357035653503, 0.26978827054257115, 0.2652738648585636, 0.2664748156481454, 0.2497117153739136, 0.2694775477432001, 0.26934767698600937, 0.2590370544226791, 0.24773092126642948, 0.24551218567821523, 0.2653810201900502, 0.24204821316746408, 0.26639286747145186, 0.2678096959359769, 0.2248785926610586, 0.23399137336421577, 0.2563397970317514, 0.25871851502604853, 0.2378280388434665, 0.2611132937345127, 0.2522978020265999, 0.23334202325539968, 0.246877733300383, 0.25759480387093375, 0.25969957998246596, 0.23173020554373727, 0.26542270901798515, 0.2530801637041446, 0.23059944302755936, 0.22198570626439867, 0.24968332418489242, 0.2572792780806452, 0.2292421302490591, 0.24588251189488153, 0.2528964586589714, 0.22329772621617391, 0.2200718806320859, 0.25530030567120626, 0.2562607601341491, 0.21092256119804184, 0.2631124206623025, 0.21186807318475265, 0.20525462205218825, 0.23895739239131417, 0.1539733465279841, 0.17809675468402447, 0.16261730087281354, 0.25130469881738454, 0.1557453607727396, 0.12153268925935673, 0.16790369163911456, 0.21944646761926695, 0.12766779733970796, 0.13915504509438473, 0.2117791198620243, 0.04174285549997124, 0.047720319119468384, 0.056490875417558754, 0.1311222902044334, 0.09667644956488773, 0.08141800645315415, 0.12182850823298323, 0.10453561876678556, 0.09990461411320341, 0.09817180669167584, 0.1360489359159612, 0.14900641828447525, 0.08863205614772861, 0.14420493419902133, 0.13625053736674592, 0.11944073021463349, 0.11982497893998834, 0.12300314940465064, 0.12516159971396318, 0.09279775698557413, 0.12536093243050211, 0.09211722740007518, 0.11341807965747495, 0.10776467014096618, 0.08628083887835845, 0.10321599070113574, 0.06025659797991648, 0.10454590062147147, 0.09882133758015989, 0.09659595072490175, 0.09831877421361256, 0.09782973384909242, 0.10084205457836043, 0.09900126327450749, 0.10571643922118092, 0.08920333387353942, 0.08256862203634256, 0.0757957664075814, 0.07723759008235273, 0.1337816080257101, 0.14087470741080949, 0.1491657404135175, 0.14803744320162834, 0.16305139062288093, 0.1500734565155837, 0.13850528715054491, 0.13461524906365344, 0.14338406625587047, 0.16777895770367954, 0.15737028738222855, 0.16086834877013104, 0.16748268342735056, 0.18991706712866002, 0.20352654864068698, 0.19765963771542344, 0.2539960204024995, 0.2041273076993638, 0.21944294914706672, 0.21425955984997933, 0.22232049572435686, 0.23312909533159126, 0.17336894008249862, 0.23871196577171572, 0.21926177978255484, 0.23377172126455428, 0.21890293388706977, 0.22186227847217352, 0.24951167329757712, 0.2138920450861929, 0.2683774239279413, 0.2527821095431933, 0.25124419382732466, 0.26397065206834025, 0.2688834299367107, 0.2857251525969169, 0.24627788846174317, 0.263653685346745, 0.25840558757669807, 0.258102538801177, 0.26700695499611937, 0.28177286128095896, 0.2858572315643978, 0.26311937095565713, 0.2844516070157893, 0.275220711827967, 0.26483806129297477, 0.2647639062334984, 0.26841807365784504, 0.2935277537962256, 0.259897107258253, 0.2734385329362561, 0.293204525543588, 0.2617756408424573, 0.23937285762569974, 0.2703243617574232, 0.28053839759430543, 0.25512371010521717, 0.28369313765209725, 0.26288661053158124, 0.281756610963268, 0.2901662063851352, 0.2940924686003594, 0.29662736873267, 0.2814792789750251, 0.2923548314990808, 0.28448968423837134, 0.2889154539543769, 0.28882165338693794, 0.2922126558681421, 0.29458052605542145, 0.2813691510105779, 0.29052317797586025, 0.2842983697259984, 0.28799014124569106, 0.2886643066499726, 0.30501873388294315, 0.34177219162376116, 0.331667518487778, 0.3158713906877719, 0.3137771433951127, 0.3272613051245192, 0.3163398958350436, 0.2816324724110372, 0.27160988012167553, 0.2703522741249991, 0.2784002922317301, 0.2813076925952672, 0.2778245120654919, 0.2819760320428419, 0.28895933403235285, 0.2928973058625102, 0.2723773998978427, 0.2856700019665142, 0.2695949996063949, 0.27152597212485197, 0.2801856806228233, 0.27945458200902035, 0.2810330660785501, 0.2568480350565098, 0.28256544431240416, 0.26657679360981423, 0.26352338742670833, 0.2541060352325912, 0.27122012126246847, 0.28061614586922523, 0.25105706875734535, 0.2752457247473136, 0.2584100744160429, 0.26910430699917687, 0.26678140904630343, 0.2702210797693538, 0.2749131326470018, 0.2670220626849396, 0.2811853643050355, 0.22813322306828449, 0.22928717481356137, 0.23144374115172506, 0.2698182856230233, 0.2983212957546598, 0.24675000533702116, 0.2452823765751047, 0.25630207076999545, 0.28058181432611984, 0.26839920739419665, 0.23341431536487572, 0.2731938107054592, 0.22687053118642234, 0.2335694115375171, 0.22680616831343423, 0.23088858201305326, 0.231856309089292, 0.23687048179656778, 0.2379154379805229, 0.233164360006536, 0.2734682779522206, 0.26432511335960585, 0.2691528341624459, 0.26675166761295366, 0.2800609457626266, 0.28904492966907425, 0.28064846767099694, 0.28072344233572427, 0.2737211869538087, 0.2889558960840234, 0.3078754097988206, 0.30967108492881423, 0.30589792103455843, 0.31074580039385113, 0.29855537752628747, 0.3012961364188172, 0.300683786727204, 0.30035789051965744, 0.30528989555295166, 0.30248751544699337, 0.31278856370132, 0.3016022352145809, 0.29417060130344036, 0.2898093224218288, 0.29384074522307424, 0.2948306117840481, 0.2783332449963765, 0.280801641254672, 0.2838522007137882, 0.30020008342093124, 0.2797178044565664, 0.28154807993665976, 0.24550275199603042, 0.2519588741952737, 0.21165397599298583, 0.17615520047721184, 0.160053718168835, 0.13376826478558995, 0.12483092949217055, 0.11211457233310174, 0.11565499599946934, 0.10321571540690953, 0.10299885520199623, 0.11388940392193873, 0.12876753907508304, 0.10436160758366612, 0.1820145524938181, 0.15274853889681572, 0.14997216544467165, 0.14517880222406723, 0.11947634990800525, 0.11953432470354874, 0.08645706875780457, 0.18487329122611482, 0.18069246394529556, 0.21036505783640388, 0.2145199023072403, 0.22653077398095398, 0.19245308379483111, 0.22342660452381072, 0.2434543731672492, 0.2483878796445125, 0.2535498724793497, 0.26638718600247147, 0.23787525603807544, 0.26144506669664713, 0.2588326508649275, 0.2532927602271425, 0.2578529406147486, 0.2763439933108574, 0.27883406806725203, 0.23975352664356422, 0.27260901954694433, 0.25419736149615857, 0.28207989573340364, 0.278278399881288, 0.2742666740925578, 0.28296883295809316, 0.2852780981674344, 0.23428319952253437, 0.24357665931805067, 0.2872647581395732, 0.2621634400040669, 0.2644876877205025, 0.27037931354874756, 0.273591510816031, 0.28364221464508355, 0.27063439120229343, 0.2699462365592321, 0.32306101214481703, 0.3052387141979771, 0.2966755004094214, 0.3008170951683939, 0.2971898762385806, 0.2918293331690837, 0.29424502663739543, 0.2859653927463928, 0.2674514787995222, 0.269409595314199, 0.2832946733795531, 0.27730425437624334, 0.274678933908999, 0.2763668880184175, 0.2769145005208333, 0.2892736693497633, 0.2738914605835728, 0.2914192845160294, 0.267387382656999, 0.27497316023276996, 0.2663430099379163, 0.27328022490143694, 0.275161150089833, 0.2585749229544578, 0.27000055073398266, 0.2541347376169746, 0.2274770524754069, 0.22485320712921333]

