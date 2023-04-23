# coding:utf-8
"""
@file: merge_index.py
@author: wu hao
@time: 2022/10/12 19:50
@env: 封城数据处理
@desc:
@ref:
"""
import csv

import pandas as pd


# 城市迁徙指数数据保存路径 in
from tqdm import tqdm

migration_index_in_old = 'F:/百度迁徙数据_日常维护/迁徙指数_最终版/in/'
# 城市迁徙指数数据保存路径 out
migration_index_out_old = 'F:/百度迁徙数据_日常维护/迁徙指数_最终版/out/'

migration_index_in_new = 'F:/百度迁徙数据_日常维护/迁徙指数_需补充/in/'

migration_index_out_new = 'F:/百度迁徙数据_日常维护/迁徙指数_需补充/out/'


migration_index_in_final = 'F:/百度迁徙数据_日常维护/迁徙指数_最终版/in/'

migration_index_out_final = 'F:/百度迁徙数据_日常维护/迁徙指数_最终版/out/'

def merge_index(migration_index_old,migration_index_new,migration_index_finall,type):
    """
    合并迁徙指数
    :param migration_index_old:  迁徙指数_最终版
    :param migration_index_new: 迁徙指数_需补充
    :param migration_index_finall: 迁徙指数_最终版/
    :param type:  类型
    :return:
    """
    file = csv.reader(open('ChinaAreaCodes.csv',encoding="utf-8"))
    for row in tqdm(file,desc="合并速度",total=375):
        if row[0] != 'code':
            code = row[0]
            name = row[1]
            index_old = migration_index_old + '{}_{}_{}.csv'.format(code, name, type)
            index_new = migration_index_new+ '{}_{}_{}.csv'.format(code, name,type)

            data_one= pd.read_csv(index_old)
            data_two = pd.read_csv(index_new)

            df = [data_one,data_two]

            result = pd.concat(df)
            result.drop_duplicates(subset=['date', 'index'], keep='first', inplace=True)
            result.sort_values(by=["date"],axis=0,ascending=False,inplace=True)
            result.to_csv(migration_index_finall+ '{}_{}_{}.csv'.format(code, name, type), index=False)

def drop_repeat_index():
    file = csv.reader(open('ChinaAreaCodes.csv',encoding="utf-8"))
    for row in tqdm(file,desc="合并速度",total=375):
        if row[0] != 'code':
            code = row[0]
            name = row[1]
            df = pd.read_csv(migration_index_in_final+ '{}_{}_{}.csv'.format(code, name, "move_in"))
            df.drop_duplicates(subset=['date','index'],keep='first',inplace=True)
            df.to_csv(migration_index_in_final+ '{}_{}_{}.csv'.format(code, name, "move_in"), index=False)





if __name__ == '__main__':

    #合并迁徙指数
    merge_index(migration_index_in_old,migration_index_in_new,migration_index_in_final,"move_in")
    merge_index(migration_index_out_old,migration_index_out_new,migration_index_out_final,"move_out")



    # drop_repeat_index()

