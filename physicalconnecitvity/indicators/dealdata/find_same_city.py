#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/12 12:54
# @Author  : wuhao
# @Email   : guess?????
# @File    : find.py
from functools import reduce

import pandas as pd
down_add_List = ["0101-0102addEdgesValue.csv","0104-0105addEdgesValue.csv ","0110-0111addEdgesValue.csv"]#"0112-0113addEdgesValue.csv "
down_remove_List = ["0101-0102removeEdgesValue.csv","0104-0105removeEdgesValue.csv ","0110-0111removeEdgesValue.csv"]#"0112-0113removeEdgesValue.csv "

up_add_List = ["0102-0103addEdgesValue.csv","0103-0104addEdgesValue.csv","0115-0116addEdgesValue.csv"] #,"0114-0115addEdgesValue.csv" ,"0109-0110addEdgesValue.csv" ,

up_remove_List = ["0103-0104removeEdgesValue.csv","0109-0110removeEdgesValue.csv",
                 "0115-0116removeEdgesValue.csv","0111-0112removeEdgesValue.csv","0113-0114removeEdgesValue.csv"] #,"0114-0115removeEdgesValue.csv"


filename_path = "D:\\04python project\\01-爬虫-爬取百度迁徙数据\\physicalconnecitvity\\" \
                "indicators\\data\\finall_data\\diff_degree\\"

def find_same_city(datafomat_list):
    dfs = []
    for dataformat in datafomat_list:
        data_format_one = pd.read_csv(filename_path+dataformat )
        df1 = data_format_one['city_name']  # 'freq'是要取交集的列的列名
        dfs.append(df1)
    return  reduce(lambda x, y: pd.merge(x, y, how='inner'), dfs)  # df_final仍然是dataframe

print("down_add_List,,diversity下降但是网络增加边的相同城市:",find_same_city(down_add_List))
print("down_remove_List,,diversity下降但是网络减少边的相同城市:",find_same_city(down_remove_List))
print("up_add_List,,diversity上升但是网络增加边的相同城市:",find_same_city(up_add_List))
print("up_remove_List,,diversity上升但是网络减少边的相同城市:",find_same_city(up_remove_List))
