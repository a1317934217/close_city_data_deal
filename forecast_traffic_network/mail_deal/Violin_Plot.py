# coding:utf-8
"""
@file: Violin_Plot.py
@author: wu hao
@time: 2023/9/4 15:14
@env: 封城数据处理
@desc:
@ref:
"""
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score
from sklearn.utils import resample






def merge_dataSet():
    file_front="F:/封城数据处理/forecast_traffic_network/data/dataset/"
    data_01 = pd.read_csv(file_front+'dataset_20210101.csv')
    data_02 = pd.read_csv(file_front+'dataset_20210102.csv')
    data_03 = pd.read_csv(file_front+'dataset_20210103.csv')
    data_04 = pd.read_csv(file_front+'dataset_20210104.csv')
    data_08 = pd.read_csv(file_front+'dataset_20210108.csv')
    data_09 = pd.read_csv(file_front+'dataset_20210109.csv')
    data_10 = pd.read_csv(file_front+'dataset_20210110.csv')
    data_11 = pd.read_csv(file_front+'dataset_20210111.csv')
    data_12 = pd.read_csv(file_front+'dataset_20210112.csv')

    data = pd.concat([data_01, data_02, data_03, data_04, data_08, data_09, data_10, data_11, data_12], ignore_index=True)

    # data['hub_promoted_index'] = pd.to_numeric(data['hub_depressed_index'], errors='coerce')

    # 假设你有两个类别，分别为正类别和负类别
    positive_samples = data[data['flag'] == 1]
    negative_samples = data[data['flag'] == 0]


    # 下采样负类别样本
    num_samples = len(negative_samples)
    positive_samples_downsampled = resample(positive_samples, replace=False, n_samples=num_samples, random_state=42)

    # 合并下采样后的样本
    downsampled_data = pd.concat([negative_samples, positive_samples_downsampled])

    downsampled_data.reindex()


    downsampled_data.to_csv('F:/封城数据处理/forecast_traffic_network/data/'
                            'dataset/experiment_data/merge_data.csv', index=False)

    # return downsampled_data


if __name__ == '__main__':

    data_result = merge_dataSet()



