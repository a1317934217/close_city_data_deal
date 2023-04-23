import pandas as pd
import csv
import datetime

# 数据处理 迁出

# 日期时间递增 格式yyyymmdd
from tqdm import tqdm


def getdaylist(beginDate,endDate):
    beginDate = datetime.datetime.strptime(str(beginDate), "%Y%m%d")
    endDate = datetime.datetime.strptime(str(endDate), "%Y%m%d")
    dayList = []
    while beginDate <= endDate:
        dayList.append(datetime.datetime.strftime(beginDate, "%Y%m%d"))
        beginDate += datetime.timedelta(days=+1)
    return dayList
#得到时间
######在这里修改要处理的时间的数据
def merge_moveOut_data(beginData,endData):
    dayList = getdaylist(beginData,endData)
    # dayList = ["20210731","20210831","20210930"]
    for i in tqdm(range(len(dayList)),desc="move_out处理进度",total=len(dayList)):
        # print("数据处理时间：",dayList[i])
        # 城市代码
        with open('ChinaAreaCodes.csv','r', encoding= 'utf-8', newline='') as csv_chinaCityCode:
            lines = csv_chinaCityCode.readlines()[1:]
            chinaCityCode = csv.reader(lines)
            # 表头
            field_order_move_in = ["city_name", 'city_id_name', 'num']
            # 开始写入数据
            with open("F:/百度迁徙数据/比例和指数计算完成后的数据/out/" + dayList[i] + ".csv", 'w', encoding="utf-8", newline='') as csvfile:
                writer = csv.DictWriter(csvfile, field_order_move_in)
                writer.writeheader()
                for csv_row in chinaCityCode:
                    # 循环打开文件 百度迁徙指数 迁入
                    # 示例：F:\01大连民族\百度迁徙爬取和数据\21年7月1日开始的前夕数据处理\百度迁徙数据爬取\迁徙指数\in\110000_北京_move_in.csv
                    #注意：一个迁徙指数文件需要和多个迁徙比例文件做数据处理
                    try:
                        baiduMigrationIndex = pd.read_csv("F:/百度迁徙数据_日常维护/迁徙指数_需补充/out/"""+csv_row[0]+"_"+csv_row[1]+"_move_out.csv",encoding="utf-8")
                        # baiduMigrationIndex = pd.read_csv("F:\\01大连民族\\迁徙数据工程\\封城数据处理\\migrate_data\\migrate_index\\out\\"""+csv_row[0]+"_"+csv_row[1]+"_move_out.csv",encoding="utf-8")
                    except Exception as problem:
                        print("error打开迁徙指数有问题：",problem)
                    # 循环打开文件 百度迁徙比例 迁入
                    # 示例：F:\01大连民族\百度迁徙爬取和数据\21年7月1日开始的前夕数据处理\百度迁徙数据爬取\迁徙比例\in\110000_北京_move_in_20210701.csv
                    try:
                        baiduMigrationProportion = pd.read_csv("F:/百度迁徙数据_日常维护/迁徙比例/out/"""+csv_row[0]+"_"+csv_row[1]+"_move_out_"+dayList[i]+".csv",encoding="gbk")
                    except Exception as problem:
                        print("error打开迁徙比例有问题：", problem)
                    # 定位到某天的一整行
                    migrationIndexDataCol = baiduMigrationIndex.loc[baiduMigrationIndex['date'] == int(dayList[i])]

                    # print("migrationIndexDataCol",migrationIndexDataCol)
                    # 定位到某天的前夕规模指数
                    migrationIndexData=float(migrationIndexDataCol["index"])

                    # print("migrationIndexData", migrationIndexData)
                    for row_migrationProportion in baiduMigrationProportion.iterrows():
                        # 取到某一天的所有城市名称
                        migrationProportionCity = row_migrationProportion[1]['city_name']
                        # 取到某一天的此城市的迁徙比例
                        migrationProportion = row_migrationProportion[1]['value']
                        #循环取值进行相乘得到最终结果
                        lastValue = migrationProportion * migrationIndexData
                        if migrationProportionCity.endswith("市"):
                            migrationProportionCity = migrationProportionCity[:-1]
                        # print(lastValue)
                        # ""+csv_row[1]+"", ""+cityName+"", ""+str(lastValue)+""]
                        row = {"city_name":csv_row[1],"city_id_name": migrationProportionCity,"num":lastValue}
                        writer.writerow(row)
            csvfile.close()
        csv_chinaCityCode.close()

if __name__ == '__main__':
    merge_moveOut_data(20230221,20230413)