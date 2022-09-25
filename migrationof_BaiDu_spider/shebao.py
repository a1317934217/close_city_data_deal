#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/17 22:47
# @Author  : wuhao
# @Email   : guess?????
# @File    : shebao.py
#coding: utf-8
import pandas as pd
import csv
import datetime
# 数据处理 迁入
import openpyxl
import xlwings as xw
import xlwings as xw
import pandas as pd
excel_file = '202102-202202.xlsx'
data = pd.read_excel(excel_file, index_col='序号')
price = data['缴费金额(元)']
num =0
for i in price:
    if "," in i:
        c = i.replace(",","")
        num = num +float(c)
    else:
        num =num +float(i)
print(num)
#44578.5
