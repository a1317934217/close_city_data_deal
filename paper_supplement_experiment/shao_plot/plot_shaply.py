# coding:utf-8
"""
@file: plot_shaply.py
@author: wu hao
@time: 2023/3/14 17:16
@env: 封城数据处理
@desc:
@ref:
"""
import xgboost as xgb
import shap
import pandas as pd
import matplotlib.pyplot as plt



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
scores.mean()
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
# shap.summary_plot(shap_values, data_x,show=False)
# plt.savefig("shap1213.jpg")
# #%%
# shap_values
# #%%
shap.summary_plot(shap_values, data_x, plot_type="bar")