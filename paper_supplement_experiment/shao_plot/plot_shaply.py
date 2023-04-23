# coding:utf-8
"""
@file: plot_shaply.py
@author: wu hao
@time: 2023/3/14 17:16
@env: 封城数据处理
@desc:
@ref:
"""
from array import array

import xgboost as xgb
import shap
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator

from sklearn.preprocessing import MinMaxScaler

import matplotlib.pyplot as plt
import numpy as np


def plot_shap_and_bar():

    data = pd.read_csv('data.csv')
    data_copy = data.copy()
    del data_copy['City_name']

    data_x = data_copy.copy()
    del data_x['eco_value']
    data_y = data_copy['eco_value']
    #%%
    # data_x
    # #%%
    # data_y
    # #%%
    #
    from sklearn.model_selection import cross_val_score
    model = xgb.XGBRegressor(max_depth=6,learning_rate=0.05,n_estimators=100,randam_state=42)
    model.fit(data_x,data_y)


    scores = cross_val_score(model, X=data_x, y=data_y, verbose=0, cv = 5, scoring='neg_mean_squared_error')
    print(scores.mean())
    #  -1.9411996002939156

    # #%%
    # explainer = shap.TreeExplainer(model)
    # # compute SHAP values




    plt.figure(dpi=450) # 设置图片的清晰度
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.xlabel('影响数值', fontsize=20)#设置x轴标签和大小


    fig = plt.gcf() # 获取后面图像的句柄
    explainer = shap.Explainer(model, data_x)
    shap_values = explainer(data_x)
    #
    # #shap图示
    # shap.summary_plot(shap_values, data_x,show=False)
    # plt.savefig("shap1213.jpg")
    #
    # #柱状图
    shap.summary_plot(shap_values, data_x, plot_type="bar")




def plot_Box_diagram(RandomForestRegressor_MSE,RandomForestRegressor_MAE,RandomForestRegressor_MSLE,
                     LinearRegression_MSE,LinearRegression_MAE,LinearRegression_MSLE,
                     KNeighborsRegressor_MSE,KNeighborsRegressor_MAE,KNeighborsRegressor_MSLE,
                     SVRZ_MSE,SVRZ_MAE,SVRZ_MSLE,
                     Ridge_MSE,Ridge_MAE,Ridge_MSL,
                     Lasso_MSE,Lasso_MAE,Lasso_MSLE,
                     xgboost_MSE,xgboost_MAE,xgboost_MSLE,
                     name_list):
    """
    带有三个子图的箱线图
    :param RandomForestRegressor_MSE:
    :param RandomForestRegressor_MAE:
    :param RandomForestRegressor_MSLE:
    :param LinearRegression_MSE:
    :param LinearRegression_MAE:
    :param LinearRegression_MSLE:
    :param KNeighborsRegressor_MSE:
    :param KNeighborsRegressor_MAE:
    :param KN eighborsRegressor_MSLE:
    :param SVRZ_MSE:
    :param SVRZ_MAE:
    :param SVRZ_MSLE:
    :param Ridge_MSE:
    :param Ridge_MAE:
    :param Ridge_MSL:
    :param Lasso_MSE:
    :param Lasso_MAE:
    :param Lasso_MSLE:
    :param xgboost_MSE:
    :param xgboost_MAE:
    :param xgboost_MSLE:
    :return:
    """

    import matplotlib.pyplot as plt
    import numpy as np

    # 生成三组随机数据，每组数据包含七个样本
    data1 = [RandomForestRegressor_MSE,LinearRegression_MSE,KNeighborsRegressor_MSE,SVRZ_MSE,
             Ridge_MSE,Lasso_MSE,xgboost_MSE]
    data2 = [RandomForestRegressor_MAE,LinearRegression_MAE,KNeighborsRegressor_MAE,SVRZ_MAE,
             Ridge_MAE,Lasso_MAE,xgboost_MAE]
    data3 = [RandomForestRegressor_MSLE,LinearRegression_MSLE,KNeighborsRegressor_MSLE,
             SVRZ_MSLE,Ridge_MSL,Lasso_MSLE,xgboost_MSLE]

    # tool = MinMaxScaler(feature_range=(-0.00005, -0.00004))

    # MaxAbsScaler = sklearn.preprocessing.MaxAbsScaler()
    # MaxAbsScaler = MaxAbsScaler.fit(train_data)

    # data1 = tool.fit_transform(data1).reshape(-1, 1).tolist()    # 创建一个包含三个子图的画布
    # data2 = tool.fit_transform(data2).reshape(-1, 1).tolist()    # 创建一个包含三个子图的画布
    # data3 = tool.fit_transform(data3).reshape(-1, 1).tolist()    # 创建一个包含三个子图的画布
    fig, axs = plt.subplots(2, 1, figsize=(8, 7),dpi=450)

    # 在每个子图中绘制七个箱线图
    for i in range(7):
        axs[0].boxplot(data1[i], positions=[i + 1], widths=0.6,
                       showfliers= False,patch_artist=True,medianprops={'color':'black'})
        axs[1].boxplot(data2[i], positions=[i + 1], widths=0.6,
                       showfliers= False,patch_artist=True,medianprops={'color':'black'})
        # axs[2].boxplot(data3[i], positions=[i + 1], widths=0.6)

    # 设置每个子图的标题和坐标轴标签
    axs[0].set_title('机器学习模型准确度',fontsize=12)
    # axs[0].set_xticks(range(1, 8))
    # axs[0].set_xticklabels(['Box {}'.format(i) for i in range(1, 8)])
    # axs[0].set_xlabel('Boxes')
    axs[0].set_ylabel('负的平均均方误差',fontsize=12)
    axs[0].axes.xaxis.set_visible(False)
    # axs[1].set_title('Data 2')
    # axs[1].set_xticks(range(1, 8))
    # axs[1].set_xticklabels(['Box {}'.format(i) for i in range(1, 8)])
    # axs[1].set_xlabel('Boxes')
    axs[1].set_ylabel('负的平均绝对误差',fontsize=12)
    axs[1].set_xticklabels([i for i in name_list], fontsize=12)



    # axs[2].set_title('Data 3')
    # axs[2].set_xticks(range(1, 8))

    # axs[2].set_xlabel('Boxes')
    # axs[2].set_ylabel('负的均方对数误差',fontsize=12)

    plt.xticks(fontsize=12, rotation=45)
    plt.yticks(fontsize=12)
    # 自动调整子图布局
    fig.tight_layout()

    # 显示图形
    plt.savefig("box_fig.jpg")
    plt.show()


if __name__ == '__main__':
    # 随机森林回归
    # MSE
    RandomForestRegressor_MSE = [-0.72885958, -1.64425394, -1.66233517, -1.01448218, -0.69697626, -1.08653836,
                                 -0.7339584, -0.90518687, -3.95523361, -2.25863863]
    # MAE
    RandomForestRegressor_MAE = [-0.66676234, -1.02250345, -1.10656385, -0.79196325, -0.66944589, -0.8587568,
                                 -0.71296493, -0.77360039, -1.77297835, -1.33633065]
    # 负的均方对数误差 MSLE
    RandomForestRegressor_MSLE = [-6.76459961e-05, -1.57957549e-04, -1.57311119e-04, -9.61006315e-05, -6.52837319e-05,
                                  -1.04348856e-04, -7.20310966e-05, -8.76492486e-05, -3.92761861e-04, -2.14984690e-04]

    # 线性回归
    # MSE
    LinearRegression_MSE = [-0.62599193, -1.28575768, -1.8448718, -0.86360159, -0.48387347, -0.88262964, -2.28293288,
                            -0.53100154, -3.95381025, -2.44611118]
    # MAE
    LinearRegression_MAE = [-0.64365792, -0.95499882, -1.24244686, -0.7089828, -0.53646269, -0.78894868, -0.75792012,
                            -0.54237335, -1.7953905, -1.38947201]
    # 负的均方对数误差
    LinearRegression_MSLE = [-5.91672360e-05, -1.20799157e-04, -1.73841986e-04, -8.15195376e-05, -4.62707514e-05,
                             -8.35511527e-05, -2.00067420e-04, -5.10960381e-05, -3.85002622e-04, -2.37628771e-04]

    # KNN回归
    # MSE
    KNeighborsRegressor_MSE = [-0.75031683, -1.67759604, -1.65644356, -1.07114851, -0.83195248, -1.1231802, -0.8190297,
                               -0.76578218, -3.948512, -2.220388]
    # MAE
    KNeighborsRegressor_MAE = [-0.67108911, -1.06752475, -1.12356436, -0.83306931, -0.74930693, -0.88217822,
                               -0.73405941, -0.70970297, -1.768, -1.3178]
    # 负的均方对数误差
    KNeighborsRegressor_MSLE = [-7.11493085e-05, -1.58335209e-04, -1.56348466e-04, -1.01460711e-04, -7.95250051e-05,
                                -1.06717701e-04, -7.82109393e-05, -7.35408967e-05, -3.83888554e-04, -2.15419975e-04]

    # SVM
    # MSE
    SVRZ_MSE = [-0.60929598, -1.18964729, -1.58067352, -0.75504921, -0.52830595, -0.84650019, -0.64754427, -0.55593101,
                -4.16722765, -2.68168005]
    # MAE
    SVRZ_MAE = [-0.63456908, -0.90778478, -1.11817162, -0.65532822, -0.56948322, -0.77289547, -0.63103336, -0.55634292,
                -1.85611796, -1.46338852]
    # 负的均方对数误差
    SVRZ_MSLE = [-5.75462564e-05, -1.11672908e-04, -1.48736860e-04, -7.13014633e-05, -5.05645472e-05, -8.01599017e-05,
                 -6.19688822e-05, -5.34886828e-05, -4.05512885e-04, -2.60253090e-04]

    # 岭回归
    # MSE
    Ridge_MSE = [-0.67028514, -1.42935302, -1.80066232, -0.85968751, -0.49816266, -0.95279956, -0.60532004, -0.48858189,
                 -4.01626408, -2.5110941]
    # MAE
    Ridge_MAE = [-0.67077848, -1.01207657, -1.22296921, -0.7194669, -0.54783228, -0.82425484, -0.56459672, -0.51597453,
                 -1.8143251, -1.4112342]
    # 负的均方对数误差
    Ridge_MSLE = [-6.33059049e-05, -1.34288772e-04, -1.69598457e-04, -8.10925908e-05, -4.76543869e-05, -9.01792884e-05,
                  -5.75686982e-05, -4.70476978e-05, -3.91099343e-04, -2.43909514e-04]

    # Lasso 回归
    # MSE
    Lasso_MSE = [-0.68927731, -1.52025463, -1.74291902, -0.84694128, -0.52745643, -0.97763956, -0.40517924, -0.50614645,
                 -3.99317486, -2.6629739]
    # MAE
    Lasso_MAE = [-0.69021363, -1.05854793, -1.20577248, -0.71335815, -0.57039528, -0.83322235, -0.477374, -0.52756449,
                 -1.81796476, -1.45748458]
    # 负的均方对数误差
    Lasso_MSLE = [-6.50757948e-05, -1.42870271e-04, -1.64055810e-04, -7.98473610e-05, -5.04572175e-05, -9.25597484e-05,
                  -3.89212385e-05, -4.87560778e-05, -3.88976018e-04, -2.58555850e-04]

    # xgboost
    # MSE
    xgboost_MSE = [-1.57863434, -2.96017271, -3.6245124, -1.86785923, -0.82613522, -1.79168146, -0.4501676, -0.81820129,
                   -2.15811526, -1.19021971]
    # MAE
    xgboost_MAE = [-1.10933197, -1.58115493, -1.80463873, -1.17802479, -0.75617987, -1.16062608, -0.51751995,
                   -0.73490448, -1.19692432, -0.90434711]
    # 负的均方对数误差
    xgboost_MSLE = [-1.50163095e-04, -2.80500739e-04, -3.43762175e-04, -1.77645688e-04, -7.88991464e-05,
                    -1.70220802e-04, -4.31322530e-05, -7.86728046e-05, -2.11622369e-04, -1.16312065e-04]

    name_list = ["随机森林回归","线性回归","KNN回归","SVM支持向量机","岭回归","Lasso回归","Xgboost"]

    # plot_Box_diagram(RandomForestRegressor_MSE, RandomForestRegressor_MAE, RandomForestRegressor_MSLE,
    #                  LinearRegression_MSE, LinearRegression_MAE, LinearRegression_MSLE,
    #                  KNeighborsRegressor_MSE, KNeighborsRegressor_MAE, KNeighborsRegressor_MSLE,
    #                  SVRZ_MSE, SVRZ_MAE, SVRZ_MSLE,
    #                  Ridge_MSE, Ridge_MAE, Ridge_MSLE,
    #                  Lasso_MSE, Lasso_MAE, Lasso_MSLE,
    #                  xgboost_MSE, xgboost_MAE, xgboost_MSLE,name_list)

    plot_shap_and_bar()








