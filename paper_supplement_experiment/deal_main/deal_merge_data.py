# coding:utf-8
"""
@file: deal_merge_data.py
@author: wu hao
@time: 2023/5/4 21:11
@env: 封城数据处理
@desc:处理经济下降百分比中出现凹凸不平的情况
@ref:
"""
a=[1,2,3,4,5]
b=[5,4]
# # a[:]=b
# for i in range(len(b)):
#     a[i] = b[i]
#
# # a.append(b)
# print(a)



import matplotlib
import pandas as pd
import csv
import datetime
import networkx as nx
import numpy as np
# coding=utf-8
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import FuncFormatter, MaxNLocator
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import FuncFormatter, MaxNLocator
# 根据路径画图
from numpy import array
from sklearn.preprocessing import MinMaxScaler
# 日期时间递增 格式yyyymmdd
def getdaylist(beginDate,endDate):
    beginDate = datetime.datetime.strptime(str(beginDate), "%Y%m%d")
    endDate = datetime.datetime.strptime(str(endDate), "%Y%m%d")
    dayList = []
    while beginDate <= endDate:
        dayList.append(datetime.datetime.strftime(beginDate, "%Y%m%d"))
        beginDate += datetime.timedelta(days=+1)
    return dayList


def merge_data(list_one,list_two):
    """

    :param list_one: 原始列表
    :param list_two: 需要加入到第一个列表的列表
    :return:
    """
    for i in range(len(list_two)):
        if list_two[i]<=0:
            list_one[i] = list_one[i]+list_two[i]
        else:
            list_one[i] = list_one[i] - list_two[i]
    print(list_one)

print(merge_data(a,b))

first_average_new_propotion_contrast = [0.0088, 0.0351, 0.0539, 0.0683, 0.0771, 0.082, 0.0894, 0.0971, 0.1083, 0.1489, 0.1778, 0.1793, 0.1973, 0.1986, 0.1863, 0.1671, 0.1485, 0.1329, 0.1172, 0.1111, 0.1126, 0.1182, 0.1102, 0.085, 0.0414, 0.0009, -0.0243, -0.0484, -0.0692, -0.0881, -0.1074, -0.1415, -0.1564, -0.1473, -0.1654, -0.1678, -0.1459, -0.1195, -0.0993, -0.0812, -0.0847, -0.1239, -0.1452, -0.1838, -0.2152, -0.2378, -0.1839, -0.1452, -0.12, -0.0922, -0.0766, -0.0594, -0.0442, -0.0489, -0.0632, -0.0779, -0.0525, -0.0242, -0.0111, 0.0057, 0.0285, 0.0492, 0.0863, 0.1385, 0.1751, 0.2273, 0.2947, 0.3686, 0.3987, 0.428, 0.4461, 0.4644, 0.4869, 0.5044, 0.5193, 0.5385, 0.5557, 0.571, 0.5746, 0.5769, 0.5774, 0.5744, 0.5667, 0.5555, 0.541, 0.5234, 0.5107, 0.4852, 0.4486, 0.4016, 0.3615, 0.3199, 0.2858, 0.2428, 0.2003, 0.156, 0.1219, 0.0887, 0.0637, 0.036, 0.0117, -0.0088, -0.0264, -0.0438, -0.0489, -0.0464, -0.0519, -0.0634, -0.0855, -0.0817, -0.085, -0.0954, -0.1005, -0.1112, -0.1125]

first_degree_new_propotion_contrast  = [0.0346, 0.0558, 0.0766, 0.089, 0.0894, 0.0936, 0.0979, 0.1021, 0.1064, 0.1266, 0.1387, 0.135, 0.135, 0.1308, 0.1266, 0.1186, 0.1064, 0.094, 0.0736, 0.0742, 0.0619, 0.0536, 0.0448, 0.0182, -0.0092, -0.0326, -0.0467, -0.061, -0.0755, -0.09, -0.1048, -0.1208, -0.1317, -0.1366, -0.1415, -0.1359, -0.1304, -0.1202, -0.1, -0.0802, -0.0748, -0.1038, -0.1132, -0.1274, -0.1315, -0.1157, -0.1005, -0.0811, -0.067, -0.0531, -0.0439, -0.0348, -0.0216, -0.0216, -0.0216, -0.0129, 0.0, 0.0128, 0.0256, 0.0386, 0.0433, 0.048, 0.0739, 0.1154, 0.1398, 0.1799, 0.2116, 0.2324, 0.2573, 0.2792, 0.2887, 0.3025, 0.3193, 0.3403, 0.3502, 0.3629, 0.3713, 0.3814, 0.3846, 0.381, 0.3772, 0.3616, 0.3529, 0.344, 0.3286, 0.3043, 0.2956, 0.2602, 0.2368, 0.2162, 0.1899, 0.1561, 0.1412, 0.1145, 0.0926, 0.051, 0.0325, 0.0066, 0.0, -0.0205, -0.0278, -0.028, -0.0423, -0.042, -0.049, -0.0559, -0.0629, -0.0764, -0.0979, -0.0828, -0.0897, -0.0966, -0.1103, -0.1164, -0.1233]

first_edge_number_new_propotion_contrast =[0.0244, 0.0438, 0.0593, 0.0696, 0.0771, 0.0819, 0.0893, 0.0967, 0.1066, 0.1349, 0.1539, 0.1551, 0.1667, 0.1664, 0.1576, 0.1439, 0.131, 0.1206, 0.1098, 0.1066, 0.1072, 0.1115, 0.1029, 0.0828, 0.0512, 0.0219, 0.002, -0.0172, -0.0347, -0.0504, -0.0664, -0.0912, -0.1012, -0.0961, -0.1076, -0.1085, -0.0946, -0.0787, -0.0664, -0.0555, -0.0575, -0.0887, -0.1052, -0.1352, -0.1554, -0.1668, -0.1329, -0.1081, -0.0897, -0.0707, -0.0592, -0.047, -0.036, -0.0389, -0.0489, -0.0601, -0.0412, -0.0215, -0.0108, 0.0049, 0.0227, 0.0397, 0.0672, 0.1096, 0.1394, 0.1824, 0.2328, 0.2851, 0.3098, 0.3358, 0.3515, 0.3693, 0.3886, 0.4041, 0.4169, 0.435, 0.4501, 0.4647, 0.4665, 0.4674, 0.4655, 0.4599, 0.453, 0.4411, 0.4269, 0.4085, 0.3955, 0.3699, 0.3386, 0.3032, 0.2709, 0.2355, 0.2083, 0.1726, 0.1402, 0.1068, 0.0821, 0.0546, 0.0356, 0.0139, 0.0, -0.0126, -0.0236, -0.0367, -0.0444, -0.0425, -0.0462, -0.0552, -0.0739, -0.0679, -0.0695, -0.0804, -0.0856, -0.0906, -0.0901]

first_nature_connecty_new_propotion_contrast =[0.0111, 0.0316, 0.0475, 0.0582, 0.0673, 0.0719, 0.0802, 0.0882, 0.0988, 0.1284, 0.1512, 0.1562, 0.1689, 0.1693, 0.1613, 0.1481, 0.1361, 0.126, 0.117, 0.118, 0.1208, 0.129, 0.1193, 0.0981, 0.0645, 0.0329, 0.0105, -0.011, -0.0308, -0.0483, -0.0659, -0.0933, -0.1067, -0.1042, -0.1156, -0.1167, -0.1019, -0.0845, -0.0722, -0.0608, -0.0642, -0.1041, -0.1258, -0.1631, -0.1851, -0.1975, -0.1606, -0.134, -0.1141, -0.0931, -0.0794, -0.0656, -0.0536, -0.0555, -0.0652, -0.0778, -0.0568, -0.035, -0.0226, -0.0026, 0.0174, 0.0374, 0.0683, 0.119, 0.1545, 0.205, 0.2598, 0.3158, 0.3442, 0.376, 0.395, 0.417, 0.4378, 0.4553, 0.4688, 0.4898, 0.5063, 0.5238, 0.5243, 0.5244, 0.52, 0.5104, 0.5029, 0.487, 0.4696, 0.4458, 0.4284, 0.3949, 0.3582, 0.3201, 0.2845, 0.241, 0.2119, 0.1684, 0.1339, 0.097, 0.0726, 0.0357, 0.0119, -0.0186, -0.0278, -0.0383, -0.045, -0.0549, -0.062, -0.0499, -0.0442, -0.0477, -0.0615, -0.042, -0.0349, -0.0503, -0.0576, -0.0624, -0.0669]




# first_average_new_propotion = [-0.0517, -0.0862, -0.1303, -0.1749, -0.2189, -0.2496, -0.2943, -0.3317, -0.3701, -0.4353, -0.5035, -0.5366, -0.579, -0.6072, -0.5937, -0.6086, -0.6155, -0.6185, -0.6101, -0.5917, -0.5737, -0.5516, -0.5303, -0.5055, -0.4708, -0.4303, -0.3817, -0.3317, -0.2731, -0.2124, -0.1623, -0.0707, 0.0339, 0.1224, 0.255, 0.4196, 0.4942, 0.6336, 0.7559, 0.8706, 0.9676, 1.0074, 1.0415, 1.0474, 1.0419, 1.0762, 1.1014, 1.0821, 1.063, 1.0367, 0.9997, 0.9822, 1.0157, 1.0183, 1.0468, 1.0396, 1.0036, 0.866, 0.7485, 0.6653, 0.5911, 0.5176, 0.4398, 0.3937, 0.3613, 0.3443, 0.3471, 0.3023, 0.2437, 0.2087, 0.1682, 0.1348, 0.1238, 0.1037, 0.0736, 0.0566, 0.0302, 0.0112, 0.003, 0.015, 0.0468, 0.0574, 0.0792, 0.1088, 0.1383, 0.159, 0.1701, 0.1698, 0.1432, 0.1327, 0.131, 0.1401, 0.1508, 0.1602, 0.1553, 0.1458, 0.1458, 0.133, 0.1347, 0.1394, 0.1359, 0.1325, 0.0808, 0.0622, 0.0192, -0.0312, -0.0746, -0.0931, -0.0862, -0.0675, -0.0312, 0.0036, 0.0419, 0.063, 0.0729, 0.0759, 0.0295, -0.0046, -0.0439, -0.077, -0.1152, -0.1569, -0.1963, -0.2356, -0.2577, -0.2921, -0.3172, -0.3403, -0.3681, -0.4301, -0.5219, -0.6125, -0.6943, -0.7699, -0.845, -0.9103, -0.958]
first_average_new_propotion =[0.0838, 0.1182, 0.1619, 0.2061, 0.2498, 0.2806, 0.3249, 0.3622, 0.4004, 0.434, 0.4587, 0.4938, 0.5388, 0.5688, 0.5818, 0.5971, 0.604, 0.607, 0.5981, 0.5787, 0.5597, 0.5363, 0.5139, 0.4875, 0.4508, 0.4079, 0.3562, 0.3029, 0.2401, 0.1747, 0.12, 0.0543, 0.0043, -0.0784, -0.2018, -0.3557, -0.4942, -0.6336, -0.7559, -0.8706, -0.9676, -1.0074, -1.0415, -1.0474, -1.0419, -1.0762, -1.1014, -1.0821, -1.063, -1.0367, -0.9997, -0.9822, -1.0157, -1.0183, -1.0468, -1.0396, -1.0036, -0.866, -0.7485, -0.6653, -0.5911, -0.5176, -0.4398, -0.3937, -0.3613, -0.3443, -0.3471, -0.3023, -0.2437, -0.2087, -0.1682, -0.1348, -0.1238, -0.1037, -0.0736, -0.0566, -0.0302, -0.0112, -0.003, -0.015, -0.0468, -0.0574, -0.0792, -0.1088, -0.1383, -0.159, -0.1701, -0.1698, -0.1432, -0.1327, -0.131, -0.1401, -0.1508, -0.1602, -0.1553, -0.1458, -0.1458, -0.133, -0.1347, -0.1394, -0.1359, -0.1325, -0.0808, -0.0622, -0.0192, 0.0312, 0.0746, 0.0931, 0.0862, 0.0675, 0.0312, -0.0036, -0.0419, -0.063, -0.0729]

# first_degree_new_propotion =[-0.2273, -0.2682, -0.3167, -0.3575, -0.4027, -0.448, -0.4955, -0.5426, -0.5893, -0.646, -0.693, -0.7336, -0.7686, -0.8035, -0.8178, -0.8584, -0.8688, -0.8651, -0.8495, -0.8274, -0.8032, -0.7765, -0.7471, -0.7081, -0.6623, -0.6127, -0.5379, -0.4508, -0.3482, -0.2255, -0.0978, 0.0875, 0.2857, 0.5246, 0.8302, 1.3111, 1.7317, 2.6562, 3.2069, 3.3448, 3.2581, 3.0588, 2.8649, 2.7, 2.5116, 2.3191, 2.1569, 2.0182, 1.7869, 1.597, 1.411, 1.2658, 1.2169, 1.1724, 1.1556, 1.1398, 1.0928, 0.9615, 0.8214, 0.7692, 0.7213, 0.6825, 0.6136, 0.5435, 0.4965, 0.4527, 0.4503, 0.4103, 0.3727, 0.3313, 0.3, 0.2701, 0.2614, 0.2402, 0.2065, 0.1799, 0.1546, 0.1256, 0.1034, 0.098, 0.1078, 0.0918, 0.081, 0.0802, 0.0845, 0.0939, 0.0935, 0.093, 0.0685, 0.0591, 0.0498, 0.0498, 0.0498, 0.0498, 0.0541, 0.0541, 0.0541, 0.0493, 0.0402, 0.0402, 0.0402, 0.0402, 0.0221, 0.0221, 0.0132, -0.0044, -0.0216, -0.03, -0.0299, -0.0298, -0.0171, -0.0043, 0.0086, 0.0172, 0.0259, 0.0345, -0.0256, -0.0684, -0.1111, -0.1538, -0.1931, -0.2361, -0.279, -0.3219, -0.3593, -0.4026, -0.4435, -0.4825, -0.5221, -0.5752, -0.63, -0.6842, -0.7391, -0.7931, -0.8462, -0.8983, -0.9496]
first_degree_new_propotion =[0.2273, 0.2682, 0.3167, 0.3575, 0.4027, 0.448, 0.4955, 0.5426, 0.5893, 0.646, 0.693, 0.7336, 0.7686, 0.8035, 0.8178, 0.8584, 0.8688, 0.8651, 0.8495, 0.8274, 0.8032, 0.7765, 0.7471, 0.7081, 0.6623, 0.6127, 0.5379, 0.4508, 0.3482, 0.2255, 0.0978, -0.0875, -0.2857, -0.5246, -0.8302, -1.3111, -1.7317, -2.6562, -3.2069, -3.3448, -3.2581, -3.0588, -2.8649, -2.7, -2.5116, -2.3191, -2.1569, -2.0182, -1.7869, -1.597, -1.411, -1.2658, -1.2169, -1.1724, -1.1556, -1.1398, -1.0928, -0.9615, -0.8214, -0.7692, -0.7213, -0.6825, -0.6136, -0.5435, -0.4965, -0.4527, -0.4503, -0.4103, -0.3727, -0.3313, -0.3, -0.2701, -0.2614, -0.2402, -0.2065, -0.1799, -0.1546, -0.1256, -0.1034, -0.098, -0.1078, -0.0918, -0.081, -0.0802, -0.0845, -0.0939, -0.0935, -0.093, -0.0685, -0.0591, -0.0498, -0.0498, -0.0498, -0.0498, -0.0541, -0.0541, -0.0541, -0.0493, -0.0402, -0.0402, -0.0402, -0.0402, -0.0221, -0.0221, -0.0132, 0.0044, 0.0216, 0.03, 0.0299, 0.0298, 0.0171, 0.0043, -0.0086, -0.0172, -0.0259]

# first_edge_number_new_propotion =[-0.0478, -0.0738, -0.1081, -0.1429, -0.1785, -0.2031, -0.2387, -0.2675, -0.2985, -0.3458, -0.3973, -0.426, -0.4613, -0.4867, -0.4749, -0.4895, -0.4952, -0.4973, -0.4902, -0.4739, -0.4584, -0.4398, -0.4222, -0.4007, -0.3699, -0.3346, -0.2915, -0.2493, -0.2009, -0.1542, -0.118, -0.0589, 0.0087, 0.069, 0.1552, 0.2555, 0.3048, 0.3922, 0.4665, 0.5339, 0.5957, 0.6258, 0.6568, 0.6722, 0.6812, 0.7035, 0.7174, 0.7084, 0.6952, 0.679, 0.6546, 0.6442, 0.6743, 0.6852, 0.7034, 0.7029, 0.6783, 0.601, 0.5313, 0.4794, 0.4322, 0.3854, 0.3347, 0.303, 0.277, 0.2622, 0.2599, 0.2293, 0.1902, 0.1649, 0.1371, 0.1149, 0.1071, 0.0936, 0.0683, 0.0526, 0.0314, 0.015, 0.0079, 0.0149, 0.0339, 0.0399, 0.0518, 0.0688, 0.0859, 0.0978, 0.1045, 0.1029, 0.085, 0.0801, 0.0804, 0.0865, 0.0939, 0.0991, 0.0967, 0.0896, 0.0896, 0.0814, 0.0824, 0.0855, 0.0833, 0.0812, 0.0501, 0.0384, 0.0123, -0.0187, -0.046, -0.0582, -0.0559, -0.0448, -0.0216, -0.0009, 0.0218, 0.0344, 0.0407, 0.0424, -0.0045, -0.0425, -0.084, -0.1215, -0.1623, -0.2054, -0.2471, -0.2887, -0.3196, -0.3583, -0.392, -0.4249, -0.4609, -0.5164, -0.5868, -0.6573, -0.7238, -0.7873, -0.8508, -0.909, -0.9566]
first_edge_number_new_propotion =[0.0433, 0.0692, 0.1036, 0.1384, 0.1741, 0.1987, 0.2343, 0.2632, 0.2941, 0.3415, 0.3931, 0.4219, 0.4572, 0.4826, 0.4818, 0.4916, 0.4974, 0.4995, 0.4924, 0.4762, 0.4608, 0.4424, 0.425, 0.4037, 0.3731, 0.3381, 0.2953, 0.2535, 0.2055, 0.1592, 0.1235, 0.065, -0.0017, -0.0613, -0.1464, -0.2455, -0.3126, -0.3922, -0.4665, -0.5339, -0.5957, -0.6258, -0.6568, -0.6722, -0.6812, -0.7035, -0.7174, -0.7084, -0.6952, -0.679, -0.6546, -0.6442, -0.6743, -0.6852, -0.7034, -0.7029, -0.6783, -0.601, -0.5313, -0.4794, -0.4322, -0.3854, -0.3347, -0.303, -0.277, -0.2622, -0.2599, -0.2293, -0.1902, -0.1649, -0.1371, -0.1149, -0.1071, -0.0936, -0.0683, -0.0526, -0.0314, -0.015, -0.0079, -0.0149, -0.0339, -0.0399, -0.0518, -0.0688, -0.0859, -0.0978, -0.1045, -0.1029, -0.085, -0.0801, -0.0804, -0.0865, -0.0939, -0.0991, -0.0967, -0.0896, -0.0896, -0.0814, -0.0824, -0.0855, -0.0833, -0.0812, -0.0501, -0.0384, -0.0123, 0.0187, 0.046, 0.0582, 0.0559, 0.0448, 0.0216, 0.0009, -0.0218, -0.0344, -0.0407]

# first_nature_connecty_new_propotion = [-0.0523, -0.0817, -0.1205, -0.1598, -0.2005, -0.2289, -0.27, -0.3023, -0.3368, -0.3865, -0.4417, -0.4755, -0.5157, -0.5446, -0.5326, -0.5512, -0.5557, -0.5581, -0.5544, -0.5404, -0.5278, -0.5114, -0.496, -0.4751, -0.4437, -0.4066, -0.36, -0.3156, -0.262, -0.2121, -0.1767, -0.1199, -0.0473, 0.0245, 0.1313, 0.257, 0.3185, 0.4335, 0.5221, 0.6113, 0.7048, 0.7549, 0.8123, 0.8462, 0.8709, 0.9029, 0.9216, 0.9099, 0.8887, 0.8682, 0.8376, 0.8257, 0.8769, 0.9073, 0.9385, 0.9422, 0.9068, 0.8022, 0.7069, 0.6392, 0.5802, 0.5178, 0.4494, 0.4053, 0.365, 0.3405, 0.3315, 0.2929, 0.2437, 0.2115, 0.178, 0.1518, 0.138, 0.1219, 0.0902, 0.0686, 0.0423, 0.021, 0.0108, 0.0164, 0.0355, 0.0395, 0.0498, 0.0668, 0.0844, 0.0977, 0.1045, 0.1019, 0.0838, 0.0796, 0.0813, 0.0877, 0.0954, 0.1, 0.0995, 0.0908, 0.0904, 0.0822, 0.0833, 0.0861, 0.0843, 0.0825, 0.0509, 0.0406, 0.0143, -0.0183, -0.0473, -0.0623, -0.0586, -0.0458, -0.0224, -0.0019, 0.0202, 0.0332, 0.0397, 0.0417, -0.0057, -0.0429, -0.0842, -0.1216, -0.1623, -0.2052, -0.2467, -0.2883, -0.3185, -0.3576, -0.3912, -0.4235, -0.459, -0.5138, -0.5852, -0.6562, -0.7227, -0.7865, -0.8501, -0.9089, -0.9567]
first_nature_connecty_new_propotion =[0.0523, 0.0817, 0.1205, 0.1598, 0.2005, 0.2289, 0.27, 0.3023, 0.3368, 0.3716, 0.4134, 0.4481, 0.4893, 0.5189, 0.5326, 0.5512, 0.5557, 0.5581, 0.5544, 0.5404, 0.5278, 0.5114, 0.496, 0.4751, 0.4437, 0.4066, 0.36, 0.3156, 0.262, 0.2121, 0.1767, 0.1328, 0.0768, 0.0089, -0.0919, -0.2109, -0.3185, -0.4335, -0.5221, -0.6113, -0.7048, -0.7549, -0.8123, -0.8462, -0.8709, -0.9029, -0.9216, -0.9099, -0.8887, -0.8682, -0.8376, -0.8257, -0.8769, -0.9073, -0.9385, -0.9422, -0.9068, -0.8022, -0.7069, -0.6392, -0.5802, -0.5178, -0.4494, -0.4053, -0.365, -0.3405, -0.3315, -0.2929, -0.2437, -0.2115, -0.178, -0.1518, -0.138, -0.1219, -0.0902, -0.0686, -0.0423, -0.021, -0.0108, -0.0164, -0.0355, -0.0395, -0.0498, -0.0668, -0.0844, -0.0977, -0.1045, -0.1019, -0.0838, -0.0796, -0.0813, -0.0877, -0.0954, -0.1, -0.0995, -0.0908, -0.0904, -0.0822, -0.0833, -0.0861, -0.0843, -0.0825, -0.0509, -0.0406, -0.0143, 0.0183, 0.0473, 0.0623, 0.0586, 0.0458, 0.0224, 0.0019, -0.0202, -0.0332, -0.0397]








first_average_new_propotion_traditional =[-0.0413, -0.0496, -0.0563, -0.0507, -0.0448, -0.045, 0.0237, 0.0322, 0.0255, 0.0106, 0.0088, 0.0351, 0.0539, 0.0683, 0.0771, 0.082, 0.0894, 0.0971, 0.1083, 0.1489, 0.1778, 0.1793, 0.1973, 0.1986, 0.1863, 0.1671, 0.1485, 0.1329, 0.1172, 0.1111, 0.1126, 0.1182, 0.1102, 0.085, 0.0414, 0.0009, -0.0243, -0.0484, -0.0692, -0.0881, -0.1074, -0.1415, -0.1564, -0.1473, -0.1654, -0.1678, -0.1459, -0.1195, -0.0993, -0.0812, -0.0847, -0.1239, -0.1452, -0.1838, -0.2152, -0.2378, -0.1839, -0.1452, -0.12, -0.0922, -0.0766, -0.0594, -0.0442, -0.0489, -0.0632, -0.0779, -0.0525, -0.0242, -0.0111, 0.0057, 0.0285, 0.0492, 0.0863, 0.1385, 0.1751, 0.2273, 0.2947, 0.3686, 0.3987, 0.428, 0.4461, 0.4644, 0.4869, 0.5044, 0.5193, 0.5385, 0.5557, 0.571, 0.5746, 0.5769, 0.5774, 0.5744, 0.5667, 0.5555, 0.541, 0.5234, 0.5107, 0.4852, 0.4486, 0.4016, 0.3615, 0.3199, 0.2858, 0.2428, 0.241, 0.247, 0.2606, 0.2722, 0.2891, 0.3057, 0.3328, 0.3615, 0.3973, 0.4313, 0.4753]

first_degree_new_propotion_traditional =[-0.0872, -0.0872, -0.0872, -0.0776, -0.0682, -0.0588, 0.0086, 0.0172, 0.0342, 0.0386, 0.0346, 0.0558, 0.0766, 0.089, 0.0894, 0.0936, 0.0979, 0.1021, 0.1064, 0.1266, 0.1387, 0.135, 0.135, 0.1308, 0.1266, 0.1186, 0.1064, 0.094, 0.0736, 0.0742, 0.0619, 0.0536, 0.0448, 0.0182, -0.0092, -0.0326, -0.0467, -0.061, -0.0755, -0.09, -0.1048, -0.1208, -0.1317, -0.1366, -0.1415, -0.1359, -0.1304, -0.1202, -0.1, -0.0802, -0.0748, -0.1038, -0.1132, -0.1274, -0.1315, -0.1157, -0.1005, -0.0811, -0.067, -0.0531, -0.0439, -0.0348, -0.0216, -0.0216, -0.0216, -0.0129, 0.0, 0.0128, 0.0256, 0.0386, 0.0433, 0.048, 0.0739, 0.1154, 0.1398, 0.1799, 0.2116, 0.2324, 0.2573, 0.2792, 0.2887, 0.3025, 0.3193, 0.3403, 0.3502, 0.3629, 0.3713, 0.3814, 0.3846, 0.381, 0.3772, 0.3616, 0.3529, 0.344, 0.3286, 0.3043, 0.2956, 0.2602, 0.2368, 0.2162, 0.1899, 0.1561, 0.1412, 0.1145, 0.1358, 0.1465, 0.1753, 0.1987, 0.2349, 0.2603, 0.2986, 0.3427, 0.3873, 0.4406, 0.4895]

first_edge_number_new_propotion_traditional =[-0.0415, -0.0464, -0.0504, -0.0457, -0.041, -0.0402, 0.0218, 0.0302, 0.0286, 0.0215, 0.0244, 0.0438, 0.0593, 0.0696, 0.0771, 0.0819, 0.0893, 0.0967, 0.1066, 0.1349, 0.1539, 0.1551, 0.1667, 0.1664, 0.1576, 0.1439, 0.131, 0.1206, 0.1098, 0.1066, 0.1072, 0.1115, 0.1029, 0.0828, 0.0512, 0.0219, 0.002, -0.0172, -0.0347, -0.0504, -0.0664, -0.0912, -0.1012, -0.0961, -0.1076, -0.1085, -0.0946, -0.0787, -0.0664, -0.0555, -0.0575, -0.0887, -0.1052, -0.1352, -0.1554, -0.1668, -0.1329, -0.1081, -0.0897, -0.0707, -0.0592, -0.047, -0.036, -0.0389, -0.0489, -0.0601, -0.0412, -0.0215, -0.0108, 0.0049, 0.0227, 0.0397, 0.0672, 0.1096, 0.1394, 0.1824, 0.2328, 0.2851, 0.3098, 0.3358, 0.3515, 0.3693, 0.3886, 0.4041, 0.4169, 0.435, 0.4501, 0.4647, 0.4665, 0.4674, 0.4655, 0.4599, 0.453, 0.4411, 0.4269, 0.4085, 0.3955, 0.3699, 0.3386, 0.3032, 0.2709, 0.2355, 0.2083, 0.1726, 0.1814, 0.1962, 0.219, 0.2368, 0.261, 0.2847, 0.3198, 0.3561, 0.3982, 0.4367, 0.4806]

first_nature_connecty_new_propotion_traditional =[-0.0484, -0.0539, -0.0589, -0.0557, -0.0516, -0.0511, 0.0109, 0.0187, 0.0166, 0.0072, 0.0111, 0.0316, 0.0475, 0.0582, 0.0673, 0.0719, 0.0802, 0.0882, 0.0988, 0.1284, 0.1512, 0.1562, 0.1689, 0.1693, 0.1613, 0.1481, 0.1361, 0.126, 0.117, 0.118, 0.1208, 0.129, 0.1193, 0.0981, 0.0645, 0.0329, 0.0105, -0.011, -0.0308, -0.0483, -0.0659, -0.0933, -0.1067, -0.1042, -0.1156, -0.1167, -0.1019, -0.0845, -0.0722, -0.0608, -0.0642, -0.1041, -0.1258, -0.1631, -0.1851, -0.1975, -0.1606, -0.134, -0.1141, -0.0931, -0.0794, -0.0656, -0.0536, -0.0555, -0.0652, -0.0778, -0.0568, -0.035, -0.0226, -0.0026, 0.0174, 0.0374, 0.0683, 0.119, 0.1545, 0.205, 0.2598, 0.3158, 0.3442, 0.376, 0.395, 0.417, 0.4378, 0.4553, 0.4688, 0.4898, 0.5063, 0.5238, 0.5243, 0.5244, 0.52, 0.5104, 0.5029, 0.487, 0.4696, 0.4458, 0.4284, 0.3949, 0.3582, 0.3201, 0.2845, 0.241, 0.2119, 0.1684, 0.1719, 0.181, 0.2044, 0.2134, 0.234, 0.2513, 0.2924, 0.3341, 0.3842, 0.4264, 0.4732]




list_index_name_SJZ = [first_average_new_propotion, first_degree_new_propotion, first_edge_number_new_propotion, first_nature_connecty_new_propotion]

list_index_name_SJZ_contrast = [first_average_new_propotion_contrast, first_degree_new_propotion_contrast,first_edge_number_new_propotion_contrast, first_nature_connecty_new_propotion_contrast]

list_SJZ__traditional = [first_average_new_propotion_traditional, first_degree_new_propotion_traditional,
                         first_edge_number_new_propotion_traditional, first_nature_connecty_new_propotion_traditional]

# for i,j in zip(list_index_name_SJZ,list_SJZ__traditional):
#     merge_data(i,j[0:30])










# print(len(getdaylist(20201201,20210325)))
# print((getdaylist(20201201,20210325)))
#
# print(len(getdaylist(20211201,20220416)))
# print((getdaylist(20211201,20220416)))



# print((getdaylist(20211115, 20220325)))




# # 石家庄有封城日期
# listXData_Lock_sjz = getdaylist(20201201, 20210508)
# print(len(listXData_Lock_sjz))
# # 石家庄对比日期 农历   比较有可比性的时间 20221030,20230406   20221113, 20230420   20220201, 20220709
listXData_contrast_sjz = getdaylist(20211201, 20220325)
print(len(listXData_contrast_sjz))

# # 西安有封城日期
# listXData_Lock_xian = getdaylist(20211115, 20220508)
# print(len(listXData_Lock_xian))
# # 西安对比日期 农历   20210105, 20210628
listXData_contrast = getdaylist(20201123, 20210402)
# listXData_contrast = getdaylist(20201115, 20210508)
print(len(listXData_contrast))








print(getdaylist(20201201, 20210508))
print(getdaylist(20211115, 20220508))


# first_average_new_propotion = [-0.0517, -0.0862, -0.1303, -0.1749, -0.2189, -0.2496, -0.2943, -0.3317, -0.3701, -0.4353, -0.5035, -0.5366, -0.579, -0.6072, -0.5937, -0.6086, -0.6155, -0.6185, -0.6101, -0.5917, -0.5737, -0.5516, -0.5303, -0.5055, -0.4708, -0.4303, -0.3817, -0.3317, -0.2731, -0.2124, -0.1623, -0.0707, 0.0339, 0.1224, 0.255, 0.4196, 0.4942, 0.6336, 0.7559, 0.8706, 0.9676, 1.0074, 1.0415, 1.0474, 1.0419, 1.0762, 1.1014, 1.0821, 1.063, 1.0367, 0.9997, 0.9822, 1.0157, 1.0183, 1.0468, 1.0396, 1.0036, 0.866, 0.7485, 0.6653, 0.5911, 0.5176, 0.4398, 0.3937, 0.3613, 0.3443, 0.3471, 0.3023, 0.2437, 0.2087, 0.1682, 0.1348, 0.1238, 0.1037, 0.0736, 0.0566, 0.0302, 0.0112, 0.003, 0.015, 0.0468, 0.0574, 0.0792, 0.1088, 0.1383, 0.159, 0.1701, 0.1698, 0.1432, 0.1327, 0.131, 0.1401, 0.1508, 0.1602, 0.1553, 0.1458, 0.1458, 0.133, 0.1347, 0.1394, 0.1359, 0.1325, 0.0808, 0.0622, 0.0192, -0.0312, -0.0746, -0.0931, -0.0862, -0.0675, -0.0312, 0.0036, 0.0419, 0.063, 0.0729, 0.0759, 0.0295, -0.0046, -0.0439, -0.077, -0.1152, -0.1569, -0.1963, -0.2356, -0.2577, -0.2921, -0.3172, -0.3403, -0.3681, -0.4301, -0.5219, -0.6125, -0.6943, -0.7699, -0.845, -0.9103, -0.958]
first_average_new_propotion =[0.075, 0.08310000000000001, 0.10799999999999998, 0.1378, 0.1727, 0.1986, 0.23550000000000004, 0.2651, 0.29209999999999997, 0.2851, 0.2809, 0.3145, 0.3414999999999999, 0.3702, 0.39549999999999996, 0.42999999999999994, 0.4555, 0.47409999999999997, 0.4809, 0.4676, 0.44709999999999994, 0.4181, 0.4037, 0.40249999999999997, 0.4094, 0.4079, 0.3562, 0.3029, 0.2401, 0.1747, 0.12, 0.0543, 0.0043, -0.0784, -0.2018, -0.3557, -0.4942, -0.6336, -0.7559, -0.8706, -0.9676, -1.0074, -1.0415, -1.0474, -1.0419, -1.0762, -1.1014, -1.0821, -1.063, -1.0367, -0.9997, -0.9822, -1.0157, -1.0183, -1.0468, -1.0396, -1.0036, -0.866, -0.7485, -0.6653, -0.5911, -0.5176, -0.4398, -0.3937, -0.3613, -0.3443, -0.3471, -0.3023, -0.2437, -0.2087, -0.1682, -0.1348, -0.1238, -0.1037, -0.0736, -0.0566, -0.0302, -0.0112, -0.003, -0.015, -0.0468, -0.0574, -0.0792, -0.1088, -0.1383, -0.159, -0.1701, -0.1698, -0.1432, -0.1327, -0.131, -0.1401, -0.1508, -0.1602, -0.1553, -0.1458, -0.1458, -0.133, -0.1347, -0.1394, -0.1359, -0.1325, -0.0808, -0.0622, -0.0192, 0.0312, 0.0746, 0.0931, 0.0862, 0.0675, 0.0312, -0.0036, -0.0419, -0.063, -0.0729]

# first_degree_new_propotion =[-0.2273, -0.2682, -0.3167, -0.3575, -0.4027, -0.448, -0.4955, -0.5426, -0.5893, -0.646, -0.693, -0.7336, -0.7686, -0.8035, -0.8178, -0.8584, -0.8688, -0.8651, -0.8495, -0.8274, -0.8032, -0.7765, -0.7471, -0.7081, -0.6623, -0.6127, -0.5379, -0.4508, -0.3482, -0.2255, -0.0978, 0.0875, 0.2857, 0.5246, 0.8302, 1.3111, 1.7317, 2.6562, 3.2069, 3.3448, 3.2581, 3.0588, 2.8649, 2.7, 2.5116, 2.3191, 2.1569, 2.0182, 1.7869, 1.597, 1.411, 1.2658, 1.2169, 1.1724, 1.1556, 1.1398, 1.0928, 0.9615, 0.8214, 0.7692, 0.7213, 0.6825, 0.6136, 0.5435, 0.4965, 0.4527, 0.4503, 0.4103, 0.3727, 0.3313, 0.3, 0.2701, 0.2614, 0.2402, 0.2065, 0.1799, 0.1546, 0.1256, 0.1034, 0.098, 0.1078, 0.0918, 0.081, 0.0802, 0.0845, 0.0939, 0.0935, 0.093, 0.0685, 0.0591, 0.0498, 0.0498, 0.0498, 0.0498, 0.0541, 0.0541, 0.0541, 0.0493, 0.0402, 0.0402, 0.0402, 0.0402, 0.0221, 0.0221, 0.0132, -0.0044, -0.0216, -0.03, -0.0299, -0.0298, -0.0171, -0.0043, 0.0086, 0.0172, 0.0259, 0.0345, -0.0256, -0.0684, -0.1111, -0.1538, -0.1931, -0.2361, -0.279, -0.3219, -0.3593, -0.4026, -0.4435, -0.4825, -0.5221, -0.5752, -0.63, -0.6842, -0.7391, -0.7931, -0.8462, -0.8983, -0.9496]
first_degree_new_propotion =[0.1927, 0.21239999999999998, 0.24009999999999998, 0.26849999999999996, 0.3133, 0.3544, 0.3976, 0.4405, 0.48290000000000005, 0.5194000000000001, 0.5543, 0.5986, 0.6335999999999999, 0.6727, 0.6912, 0.7398, 0.7624, 0.7711, 0.7759, 0.7532, 0.7413000000000001, 0.7229, 0.7023, 0.6899, 0.6715, 0.6127, 0.5379, 0.4508, 0.3482, 0.2255, 0.0978, -0.0875, -0.2857, -0.5246, -0.8302, -1.3111, -1.7317, -2.6562, -3.2069, -3.3448, -3.2581, -3.0588, -2.8649, -2.7, -2.5116, -2.3191, -2.1569, -2.0182, -1.7869, -1.597, -1.411, -1.2658, -1.2169, -1.1724, -1.1556, -1.1398, -1.0928, -0.9615, -0.8214, -0.7692, -0.7213, -0.6825, -0.6136, -0.5435, -0.4965, -0.4527, -0.4503, -0.4103, -0.3727, -0.3313, -0.3, -0.2701, -0.2614, -0.2402, -0.2065, -0.1799, -0.1546, -0.1256, -0.1034, -0.098, -0.1078, -0.0918, -0.081, -0.0802, -0.0845, -0.0939, -0.0935, -0.093, -0.0685, -0.0591, -0.0498, -0.0498, -0.0498, -0.0498, -0.0541, -0.0541, -0.0541, -0.0493, -0.0402, -0.0402, -0.0402, -0.0402, -0.0221, -0.0221, -0.0132, 0.0044, 0.0216, 0.03, 0.0299, 0.0298, 0.0171, 0.0043, -0.0086, -0.0172, -0.0259]

# first_edge_number_new_propotion =[-0.0478, -0.0738, -0.1081, -0.1429, -0.1785, -0.2031, -0.2387, -0.2675, -0.2985, -0.3458, -0.3973, -0.426, -0.4613, -0.4867, -0.4749, -0.4895, -0.4952, -0.4973, -0.4902, -0.4739, -0.4584, -0.4398, -0.4222, -0.4007, -0.3699, -0.3346, -0.2915, -0.2493, -0.2009, -0.1542, -0.118, -0.0589, 0.0087, 0.069, 0.1552, 0.2555, 0.3048, 0.3922, 0.4665, 0.5339, 0.5957, 0.6258, 0.6568, 0.6722, 0.6812, 0.7035, 0.7174, 0.7084, 0.6952, 0.679, 0.6546, 0.6442, 0.6743, 0.6852, 0.7034, 0.7029, 0.6783, 0.601, 0.5313, 0.4794, 0.4322, 0.3854, 0.3347, 0.303, 0.277, 0.2622, 0.2599, 0.2293, 0.1902, 0.1649, 0.1371, 0.1149, 0.1071, 0.0936, 0.0683, 0.0526, 0.0314, 0.015, 0.0079, 0.0149, 0.0339, 0.0399, 0.0518, 0.0688, 0.0859, 0.0978, 0.1045, 0.1029, 0.085, 0.0801, 0.0804, 0.0865, 0.0939, 0.0991, 0.0967, 0.0896, 0.0896, 0.0814, 0.0824, 0.0855, 0.0833, 0.0812, 0.0501, 0.0384, 0.0123, -0.0187, -0.046, -0.0582, -0.0559, -0.0448, -0.0216, -0.0009, 0.0218, 0.0344, 0.0407, 0.0424, -0.0045, -0.0425, -0.084, -0.1215, -0.1623, -0.2054, -0.2471, -0.2887, -0.3196, -0.3583, -0.392, -0.4249, -0.4609, -0.5164, -0.5868, -0.6573, -0.7238, -0.7873, -0.8508, -0.909, -0.9566]
first_edge_number_new_propotion =[0.018899999999999997, 0.0254, 0.0443, 0.0688, 0.097, 0.11679999999999999, 0.14500000000000002, 0.16649999999999998, 0.18749999999999997, 0.20660000000000003, 0.2392, 0.26680000000000004, 0.2905, 0.3162, 0.32420000000000004, 0.3477, 0.3664, 0.3789, 0.3826, 0.36960000000000004, 0.35359999999999997, 0.3309, 0.3221, 0.3209, 0.32189999999999996, 0.3381, 0.2953, 0.2535, 0.2055, 0.1592, 0.1235, 0.065, -0.0017, -0.0613, -0.1464, -0.2455, -0.3126, -0.3922, -0.4665, -0.5339, -0.5957, -0.6258, -0.6568, -0.6722, -0.6812, -0.7035, -0.7174, -0.7084, -0.6952, -0.679, -0.6546, -0.6442, -0.6743, -0.6852, -0.7034, -0.7029, -0.6783, -0.601, -0.5313, -0.4794, -0.4322, -0.3854, -0.3347, -0.303, -0.277, -0.2622, -0.2599, -0.2293, -0.1902, -0.1649, -0.1371, -0.1149, -0.1071, -0.0936, -0.0683, -0.0526, -0.0314, -0.015, -0.0079, -0.0149, -0.0339, -0.0399, -0.0518, -0.0688, -0.0859, -0.0978, -0.1045, -0.1029, -0.085, -0.0801, -0.0804, -0.0865, -0.0939, -0.0991, -0.0967, -0.0896, -0.0896, -0.0814, -0.0824, -0.0855, -0.0833, -0.0812, -0.0501, -0.0384, -0.0123, 0.0187, 0.046, 0.0582, 0.0559, 0.0448, 0.0216, 0.0009, -0.0218, -0.0344, -0.0407]

# first_nature_connecty_new_propotion = [-0.0523, -0.0817, -0.1205, -0.1598, -0.2005, -0.2289, -0.27, -0.3023, -0.3368, -0.3865, -0.4417, -0.4755, -0.5157, -0.5446, -0.5326, -0.5512, -0.5557, -0.5581, -0.5544, -0.5404, -0.5278, -0.5114, -0.496, -0.4751, -0.4437, -0.4066, -0.36, -0.3156, -0.262, -0.2121, -0.1767, -0.1199, -0.0473, 0.0245, 0.1313, 0.257, 0.3185, 0.4335, 0.5221, 0.6113, 0.7048, 0.7549, 0.8123, 0.8462, 0.8709, 0.9029, 0.9216, 0.9099, 0.8887, 0.8682, 0.8376, 0.8257, 0.8769, 0.9073, 0.9385, 0.9422, 0.9068, 0.8022, 0.7069, 0.6392, 0.5802, 0.5178, 0.4494, 0.4053, 0.365, 0.3405, 0.3315, 0.2929, 0.2437, 0.2115, 0.178, 0.1518, 0.138, 0.1219, 0.0902, 0.0686, 0.0423, 0.021, 0.0108, 0.0164, 0.0355, 0.0395, 0.0498, 0.0668, 0.0844, 0.0977, 0.1045, 0.1019, 0.0838, 0.0796, 0.0813, 0.0877, 0.0954, 0.1, 0.0995, 0.0908, 0.0904, 0.0822, 0.0833, 0.0861, 0.0843, 0.0825, 0.0509, 0.0406, 0.0143, -0.0183, -0.0473, -0.0623, -0.0586, -0.0458, -0.0224, -0.0019, 0.0202, 0.0332, 0.0397, 0.0417, -0.0057, -0.0429, -0.0842, -0.1216, -0.1623, -0.2052, -0.2467, -0.2883, -0.3185, -0.3576, -0.3912, -0.4235, -0.459, -0.5138, -0.5852, -0.6562, -0.7227, -0.7865, -0.8501, -0.9089, -0.9567]
first_nature_connecty_new_propotion =[0.0412, 0.05009999999999999, 0.073, 0.1016, 0.1332, 0.15699999999999997, 0.18980000000000002, 0.2141, 0.238, 0.2432, 0.2622, 0.2919, 0.3204, 0.3496, 0.37129999999999996, 0.4031, 0.4196, 0.43210000000000004, 0.4374, 0.4224, 0.40700000000000003, 0.38239999999999996, 0.3767, 0.377, 0.3792, 0.4066, 0.36, 0.3156, 0.262, 0.2121, 0.1767, 0.1328, 0.0768, 0.0089, -0.0919, -0.2109, -0.3185, -0.4335, -0.5221, -0.6113, -0.7048, -0.7549, -0.8123, -0.8462, -0.8709, -0.9029, -0.9216, -0.9099, -0.8887, -0.8682, -0.8376, -0.8257, -0.8769, -0.9073, -0.9385, -0.9422, -0.9068, -0.8022, -0.7069, -0.6392, -0.5802, -0.5178, -0.4494, -0.4053, -0.365, -0.3405, -0.3315, -0.2929, -0.2437, -0.2115, -0.178, -0.1518, -0.138, -0.1219, -0.0902, -0.0686, -0.0423, -0.021, -0.0108, -0.0164, -0.0355, -0.0395, -0.0498, -0.0668, -0.0844, -0.0977, -0.1045, -0.1019, -0.0838, -0.0796, -0.0813, -0.0877, -0.0954, -0.1, -0.0995, -0.0908, -0.0904, -0.0822, -0.0833, -0.0861, -0.0843, -0.0825, -0.0509, -0.0406, -0.0143, 0.0183, 0.0473, 0.0623, 0.0586, 0.0458, 0.0224, 0.0019, -0.0202, -0.0332, -0.0397]



# #石家庄最新的数据和比例
first_average_new_traditional  =   [5.5, 5.858974358974359, 5.564102564102564, 5.717948717948718, 6.948717948717949, 0.0, 7.897435897435898, 7.282051282051282, 7.897435897435898, 6.461538461538462, 4.923076923076923, 4.653846153846154, 5.67948717948718, 5.461538461538462, 5.230769230769231, 5.089743589743589, 4.923076923076923, 4.833333333333333, 4.923076923076923, 5.089743589743589, 5.17948717948718, 5.0, 5.089743589743589, 4.923076923076923, 5.448717948717949, 5.538461538461538, 6.0256410256410255, 6.487179487179487, 6.653846153846154, 5.717948717948718, 5.461538461538462, 5.3076923076923075, 6.128205128205129, 5.576923076923077, 5.730769230769231, 5.358974358974359, 5.0, 5.089743589743589, 5.089743589743589, 5.269230769230769, 6.923076923076923, 6.6923076923076925, 5.064102564102564, 6.5, 5.653846153846154, 4.743589743589744, 4.653846153846154, 4.653846153846154, 5.089743589743589, 4.743589743589744, 4.397435897435898, 5.012820512820513, 4.858974358974359, 4.371794871794871, 4.205128205128205, 4.205128205128205, 4.064102564102564, 4.205128205128205, 4.205128205128205, 4.205128205128205, 4.32051282051282, 4.32051282051282, 3.7435897435897436, 4.487179487179487, 4.782051282051282, 5.4743589743589745, 5.948717948717949, 6.141025641025641, 6.397435897435898, 6.217948717948718, 6.217948717948718, 5.128205128205129, 3.128205128205128, 4.205128205128205, 3.6666666666666665, 4.487179487179487, 5.384615384615385, 7.884615384615385, 6.987179487179487, 5.833333333333333, 6.038461538461538, 5.538461538461538, 5.538461538461538, 5.358974358974359, 3.769230769230769, 3.4871794871794872, 3.5256410256410255, 6.115384615384615, 6.538461538461538, 5.538461538461538, 5.653846153846154, 5.833333333333333, 5.538461538461538, 5.910256410256411, 5.897435897435898, 5.5256410256410255, 6.3076923076923075, 7.884615384615385, 9.179487179487179, 6.589743589743589, 6.128205128205129, 4.846153846153846, 4.897435897435898, 5.17948717948718, 4.833333333333333, 4.653846153846154, 4.346153846153846, 4.128205128205129, 3.8974358974358974, 3.8333333333333335, 3.8333333333333335, 3.3846153846153846, 2.948717948717949, 2.8076923076923075, 2.5, 2.3461538461538463, 2.230769230769231, 2.269230769230769, 2.08974358974359, 2.0128205128205128, 2.2564102564102564, 1.8974358974358974, 1.8717948717948718, 1.9871794871794872, 1.9615384615384615, 2.1666666666666665, 2.2948717948717947, 2.4615384615384617, 2.230769230769231, 2.282051282051282, 2.141025641025641, 2.41025641025641, 2.41025641025641, 2.41025641025641, 2.1538461538461537, 2.3846153846153846, 2.41025641025641, 2.2948717948717947, 2.3461538461538463, 1.9743589743589745, 2.448717948717949, 2.2435897435897436, 2.2948717948717947, 2.1923076923076925, 2.1923076923076925, 2.4358974358974357, 2.7564102564102564]

first_degree_new_traditional =     [10, 10, 10, 10, 10, 0, 12, 11, 12, 12, 10, 10, 10, 11, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11, 11, 11, 12, 12, 12, 11, 10, 12, 12, 11, 10, 10, 10, 10, 10, 12, 11, 9, 10, 10, 10, 10, 10, 10, 9, 10, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 10, 11, 11, 11, 12, 12, 11, 8, 9, 9, 10, 12, 12, 12, 11, 11, 11, 11, 11, 9, 9, 10, 11, 11, 11, 10, 10, 10, 12, 12, 11, 12, 12, 12, 12, 11, 10, 10, 11, 11, 10, 9, 9, 9, 9, 8, 8, 6, 7, 7, 7, 6, 7, 5, 6, 7, 6, 5, 7, 6, 7, 6, 7, 6, 7, 6, 7, 7, 7, 7, 7, 7, 7, 7, 6, 7, 6, 7, 6, 6, 7, 7]

first_edge_number_new_traditional =     [50, 52, 50, 50, 57, 0, 62, 59, 62, 55, 46, 44, 51, 49, 48, 47, 46, 45, 46, 47, 48, 46, 47, 46, 49, 49, 52, 55, 56, 51, 49, 49, 53, 50, 50, 48, 46, 47, 47, 48, 57, 55, 46, 54, 49, 44, 43, 43, 46, 44, 41, 45, 44, 40, 39, 39, 38, 39, 39, 39, 40, 40, 36, 41, 43, 48, 51, 52, 53, 52, 52, 46, 31, 39, 35, 41, 47, 61, 56, 50, 51, 48, 48, 47, 37, 35, 35, 52, 54, 48, 49, 50, 48, 50, 50, 48, 53, 61, 67, 54, 52, 44, 45, 46, 44, 43, 41, 39, 38, 37, 37, 33, 29, 30, 27, 26, 24, 25, 23, 23, 25, 22, 21, 23, 22, 24, 25, 27, 24, 25, 24, 27, 27, 27, 24, 26, 27, 26, 26, 23, 27, 25, 25, 24, 24, 26, 28]

first_nature_connecty_new_traditional=    [5.750411981079295, 6.018512567393066, 5.766985319973946, 5.711567102194351, 6.591648172983164, 0.0, 7.202235362406284, 6.827868664213773, 7.230584467350561, 6.3640086854553966, 5.343574163181218, 5.105219715065422, 5.911930568476566, 5.629577568581174, 5.611656503765818, 5.4634536081820855, 5.343574163181218, 5.182919291326898, 5.343574163181218, 5.348822202499723, 5.509388663077221, 5.300527093100186, 5.4634536081820855, 5.343574163181218, 5.624994412282067, 5.648520274589906, 6.036209183104178, 6.4014044778883585, 6.518535955988218, 5.904145134810231, 5.629577568581174, 5.6845380952598745, 6.163342031196992, 5.771829156904455, 5.759620636015833, 5.597031428359089, 5.300527093100186, 5.4634536081820855, 5.4634536081820855, 5.564908259659555, 6.628259421052694, 6.534959078413907, 5.562041619844624, 6.428564663528827, 5.828230004376203, 5.243102892728713, 5.083169075158174, 5.083169075158174, 5.402181182307535, 5.2409268131659585, 4.853616012010378, 5.2622258032676275, 5.220403058473129, 4.525174978781859, 4.431734078473191, 4.431734078473191, 4.283514409832053, 4.431734078473191, 4.431734078473191, 4.431734078473191, 4.583847802394475, 4.583847802394475, 4.05657319602307, 4.659243263851195, 4.976749934886478, 5.749334154647477, 6.0707959576336314, 6.19557867601596, 6.325078808591349, 6.133245879292812, 6.133245879292812, 5.36047846606343, 3.2553348558547173, 4.352888348517276, 3.8549414044589394, 4.694468581048806, 5.452824686806969, 7.223745964040222, 6.616576900530718, 5.905937602770348, 6.046789352702373, 5.661319316285725, 5.661319316285725, 5.532160343817758, 4.333880055471758, 4.054474447572704, 4.054221987896424, 6.217600642423536, 6.4638497422151815, 5.661319316285725, 5.78963066888436, 5.917324897129214, 5.6453308672488465, 5.875786715859198, 5.91827251190718, 5.705253334538094, 6.323653070529472, 7.252119410055704, 8.006089432689125, 6.4588670844658225, 6.303536535435783, 5.296853571196978, 5.392029201954379, 5.39168832100981, 5.181540948020254, 5.097989097825798, 4.858549840590372, 4.5809707454694335, 4.56130090436142, 4.226469434847886, 4.270264605529008, 3.6338573115874717, 2.8695882333860308, 3.3331719653673786, 2.812370196219135, 2.7230788886237893, 2.2696277197269175, 2.5461217299518912, 2.112908983403675, 2.3073393782263643, 2.621865754215742, 2.2711666483805715, 2.0084829819289123, 2.4780862338667387, 2.193556935636658, 2.586493658354107, 2.688307487785341, 3.160525664820555, 2.475127287324306, 2.744655930244229, 2.5733977365348517, 3.219369706091864, 3.2063818771134684, 3.2063818771134684, 2.6129236959920363, 2.9327720682883993, 3.2063818771134684, 3.0230837771188503, 2.8761138483810083, 2.5955087315408987, 3.0283810527957193, 2.770780174045785, 2.554070480595228, 2.432903644984571, 2.432903644984571, 2.596174953998964, 2.9076202509834195]


# a=[1,2,3,4,5]
# b=[5,4]
# cc = b[:]
# print(b)
# print(cc)