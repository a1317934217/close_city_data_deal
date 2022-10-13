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

migration_index_in_old = 'F:/百度迁徙数据_日常维护/迁徙指数/in/'
# 城市迁徙指数数据保存路径 out
migration_index_out_old = 'F:/百度迁徙数据_日常维护/迁徙指数/out/'

migration_index_in_new = 'F:/百度迁徙数据_日常维护/迁徙指数_需补充/in/'

migration_index_out_new = 'F:/百度迁徙数据_日常维护/迁徙指数_需补充/out/'


migration_index_in_final = 'F:/百度迁徙数据_日常维护/迁徙指数_最终版/in/'

migration_index_out_final = 'F:/百度迁徙数据_日常维护/迁徙指数_最终版/out/'

def merge_index():
    file = csv.reader(open('ChinaAreaCodes.csv',encoding="utf-8"))
    for row in tqdm(file,desc="合并速度",total=375):
        if row[0] != 'code':
            code = row[0]
            name = row[1]
            index_old = migration_index_out_old + '{}_{}_{}.csv'.format(code, name, "move_out")
            index_new = migration_index_out_new+ '{}_{}_{}.csv'.format(code, name, "move_out")

            data_one= pd.read_csv(index_old)
            data_two = pd.read_csv(index_new)

            df = [data_one,data_two]

            result = pd.concat(df)
            result.sort_values(by=["date"],axis=0,ascending=False,inplace=True)
            result.to_csv(migration_index_out_final+ '{}_{}_{}.csv'.format(code, name, "move_out"), index=False)



if __name__ == '__main__':
    merge_index()

