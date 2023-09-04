# coding:utf-8
"""
@file: bar_example_result.py
@author: wu hao
@time: 2023/7/11 16:54
@env: 封城数据处理
@desc:
@ref:
"""
import matplotlib.pyplot as plt
import numpy as np

# 创建一组示例数据
# data = [np.random.normal(0, std, 100) for std in range(1, 4)]
data1 = [0.524,0.594,0.602,0.573,0.583,0.583,0.573,0.465,0.583,0.423,0.403,0.501,0.604,0.626]
data2 = [0.504,0.516,0.563,0.415,0.434,0.562,0.446,0.403,0.556,0.433,0.428,0.424,0.573,0.505]
data3 = [0.546,0.598,0.604,0.426,0.426,0.605,0.444,0.437,0.605,0.406,0.439,0.415,0.585,0.522]

plt.rcParams['font.sans-serif'] = ['SimHei']  # SimHei黑体     SimSun  宋体
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 创建箱线图
fig, ax = plt.subplots(dpi=450)
ax.boxplot([data1,data2,data3])
plt.xlim(0.1)
plt.axhline(y=0.54,color="r",linestyle="--",linewidth="1")

# 设置横轴标签
ax.set_xticklabels(['平均点连通性', '边数目', '平均最短路径长度'])

# 设置标题和标签
# ax.set_title('平均点连通性')
ax.set_xlabel('指标名称')
ax.set_ylabel('数值')

# 显示图形
plt.show()