# coding:utf-8
"""
@file: test.py
@author: wu hao
@time: 2022/12/25 17:53
@env: 封城数据处理
@desc:
@ref:
"""
import csv
import json

import requests
import xlwt
import sys
import urllib.request
import io
import bs4


#数据爬取后的位置
from tqdm import tqdm

epidemic_data_file_location = "F:/疫情搜索指数数据/整理之后数据/"
#376个地市级信息
city_location = "F:/封城数据处理/epidemic_situation_index_spider/data/ChinaAreaCodes_epidemic.csv"

def HTTP_get(url):
    headers={"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
    resp = requests.get(url=url,headers=headers)
    resp.encoding = 'utf-8'
    return resp.text

def to_Excel(date_list,search_data,health_data,title_excel,epidemic_data_file_location):
    """
    :param date_list: 日期
    :param search_data: 疫情搜索指数
    :param health_data: 健康问诊指数
    :param title_excel: 生成的excel名称
    :param epidemic_data_file_location: 文件保存的位置
    :return:
    """
    # 表头
    field_order_move_in = ["date", '百度疫情搜索指数', '百度健康问诊指数']
    # 开始写入整理完的数据csv
    with open(epidemic_data_file_location+title_excel+".csv", 'w',encoding="utf-8", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, field_order_move_in)
        writer.writeheader()
        for date,search,health in zip(date_list,search_data,health_data):
            row = {"date": date, "百度疫情搜索指数": search, "百度健康问诊指数": health}
            writer.writerow(row)
        csvfile.close()


def spider_city():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')  # 改变标准输出的默认编码
    problem_list =[]
    file = csv.reader(open(city_location,encoding="utf-8"))
    for row in tqdm(file,desc="疫情搜索指数爬取进度",total=371):
        if row[0] != 'code':
            name = row[1]
            try:
                # 全国31个省市的疫情搜索比例
                # url = 'https://events.baidu.com/api/ncov/indexlist?callback=jsonp_1671962219776_90684'

                #其余城市的疫情搜索指数
                url = "https://www.baidu.com/s?sa=re_1_51677&wd={}市疫情指数&rsv_pq=9cf860e800136735&oq=疫情搜索指数&rsv_t=299bc/M9vO7tiAqmufnhJCQgK1H+V2+f9BQxMZeDvjyNvjSuBgGSPzqfpMgdi9uDOLMZ&tn=baiduhome_pg&ie=utf-8".format(name)

                try:

                    headers = {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                        'Cookie': 'BIDUPSID=3505364E871DBCF319777DA02E402DAD; PSTM=1664017249; BAIDUID=3505364E871DBCF31D5A705FC4E1E125:FG=1; BD_UPN=12314753; BDUSS=lpMkdQRHRaOWxSRUQ5UnBmNy11RTdabi1ab0Y0cjZPN2Z3SjY5b1ZsdEV2RmRqRVFBQUFBJCQAAAAAAAAAAAEAAAD15IanYTEzMTc5MzQyMTcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEQvMGNELzBjcX; BDUSS_BFESS=lpMkdQRHRaOWxSRUQ5UnBmNy11RTdabi1ab0Y0cjZPN2Z3SjY5b1ZsdEV2RmRqRVFBQUFBJCQAAAAAAAAAAAEAAAD15IanYTEzMTc5MzQyMTcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEQvMGNELzBjcX; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDSFRCVID=TstOJeC62AYxpnTjmKQsMt89F2l-BRRTH6ao89et6MAAoQqyNS1KEG0PBM8g0KAMQgRUogKKQeOTHAkF_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF=tbKJ_CIXtC83fP36q4Q2MtKe22T22jnn-5n9aJ5nJDoNotnxhlO8hfPuKPcJqTcltDtL5fo4QpP-HJA9etoMjxuFLfnIbRcwLb6iKl0MLpoYbb0xyUQY0t-w3fnMBMnI5mOnapjo3fAKftnOM46JehL3346-35543bRTLnLy5KJtMDcnK4-Xj6o3ea7P; BAIDUID_BFESS=3505364E871DBCF31D5A705FC4E1E125:FG=1; BDSFRCVID_BFESS=TstOJeC62AYxpnTjmKQsMt89F2l-BRRTH6ao89et6MAAoQqyNS1KEG0PBM8g0KAMQgRUogKKQeOTHAkF_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF_BFESS=tbKJ_CIXtC83fP36q4Q2MtKe22T22jnn-5n9aJ5nJDoNotnxhlO8hfPuKPcJqTcltDtL5fo4QpP-HJA9etoMjxuFLfnIbRcwLb6iKl0MLpoYbb0xyUQY0t-w3fnMBMnI5mOnapjo3fAKftnOM46JehL3346-35543bRTLnLy5KJtMDcnK4-Xj6o3ea7P; delPer=0; BD_CK_SAM=1; BA_HECTOR=8g2l0084ag0galag25a084h61hqgg6m1j; BDRCVFR[feWj1Vr5u3D]=mk3SLVN4HKm; H_WISE_SIDS=188748_204906_209307_211986_213042_213355_214797_215730_216839_219943_219946_222216_222624_223064_224267_226628_227870_227932_228650_229154_229812_229968_230175_230930_231979_232249_232356_232403_232777_233836_234044_234050_234295_234426_234722_234769_234815_234927_235174_235200_235373_235443_235473_235512_235979_236237_236242_236433_236517_236537_236615_236653_236811_237240_237446_237819_237837_237964_238148_238226_238266_238410_238506_238510_238565_238630_238756_239005_239007_239101_239145_239281_239605_239706_239760_239947_240016_240036_240103_240225_240305_240395_240447_240465_240597_240649_240782_240889_240937_241044_241153_241178_241207_241232_241249_241296_241347; H_WISE_SIDS_BFESS=188748_204906_209307_211986_213042_213355_214797_215730_216839_219943_219946_222216_222624_223064_224267_226628_227870_227932_228650_229154_229812_229968_230175_230930_231979_232249_232356_232403_232777_233836_234044_234050_234295_234426_234722_234769_234815_234927_235174_235200_235373_235443_235473_235512_235979_236237_236242_236433_236517_236537_236615_236653_236811_237240_237446_237819_237837_237964_238148_238226_238266_238410_238506_238510_238565_238630_238756_239005_239007_239101_239145_239281_239605_239706_239760_239947_240016_240036_240103_240225_240305_240395_240447_240465_240597_240649_240782_240889_240937_241044_241153_241178_241207_241232_241249_241296_241347; SE_LAUNCH=5:1672019516; BDPASSGATE=IlPT2AEptyoA_yiU4VKY3kIN8efRNLm4Aeu0S6plBVW4fCWWmhH3BrUzWz0HSieXBDP6wZTXdMsDxXTqXlVXa_EqnBsZolpOaSaXzKGoucHtVM69-t5yILXoHUE2sA8PbRhL-3MEF32EMWosyBDxhvwPisqJyeRhmfr55EDHiMzcGICoYHn2zIKYNnRmOHfEK2328wXxd5NPMVCCROLVLj87hCM9QJ1L70aOatY6C3DzyEQ4Bw4aYfYDCnXd38t13Ai7GwaLxKSl2yU5q-2YSkgtbUbj-_faO5MMAavxlMREN0DtT_H0Li8uKqcmwge; PSINO=2; H_PS_PSSID=37781_36542_37975_37645_37556_37520_37689_37908_36804_37948_37938_37901_26350_37959_37790_37881; H_PS_645EC=c19drKZI2PENKAep9kz4lZvwoZ3t3S65ZFjwutarswMqgR2s8gHnyyI0cFeLF2ecY5Wp'
                    }
                    # 浏览器取到数据
                    resp = requests.get(url=url, headers=headers)
                    resp.encoding = 'utf-8'
                    # 转为html数据
                    needDeal_html = resp.text
                    # BS4爬取网页数据
                    soup = bs4.BeautifulSoup(needDeal_html, 'html.parser')
                    # 获取到div数据块
                    divneed = soup.find("div", class_="_aladdin_13t8f_1 ms-epidemic-exp-san_6pupP group_5Cqz4")
                    # 字符串拼接取到注释的   疫情搜索比例和 健康指数
                    aa = str(divneed).split("s-data:")
                    cc = aa[1].split("-->")
                    # str 转为json
                    jsonData = json.loads(cc[0])
                    # 整理数据
                    data_list = []
                    data_list_needDeal = jsonData["trendData"]["dayData"]["xAxisData"]
                    for i in data_list_needDeal:
                        data_list.append("2022" + i.replace(".", ""))
                    header_list = jsonData["trendData"]["dayData"]["lineNames"]
                    health_data = jsonData["trendData"]["dayData"]["seriesDatas"][0]
                    search_data = jsonData["trendData"]["dayData"]["seriesDatas"][1]
                    title_excel = jsonData["title"]
                    to_Excel(data_list,search_data,health_data,title_excel,epidemic_data_file_location)
                except Exception as reason:
                    problem_list.append(name)
                    print(name,reason)
            except Exception as why:
                print(why)
    return problem_list

def return_spider(list):
    problem_list=[]
    for cityname in list:
        try:
            # 全国31个省市的疫情搜索比例
            # url = 'https://events.baidu.com/api/ncov/indexlist?callback=jsonp_1671962219776_90684'

            # 其余城市的疫情搜索指数
            url = "https://www.baidu.com/s?sa=re_1_51677&wd={}&rsv_pq=9cf860e800136735&oq=疫情搜索指数&rsv_t=299bc/M9vO7tiAqmufnhJCQgK1H+V2+f9BQxMZeDvjyNvjSuBgGSPzqfpMgdi9uDOLMZ&tn=baiduhome_pg&ie=utf-8".format(
                cityname)

            try:

                headers = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                    'Cookie': 'BIDUPSID=3505364E871DBCF319777DA02E402DAD; PSTM=1664017249; BAIDUID=3505364E871DBCF31D5A705FC4E1E125:FG=1; BD_UPN=12314753; BDUSS=lpMkdQRHRaOWxSRUQ5UnBmNy11RTdabi1ab0Y0cjZPN2Z3SjY5b1ZsdEV2RmRqRVFBQUFBJCQAAAAAAAAAAAEAAAD15IanYTEzMTc5MzQyMTcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEQvMGNELzBjcX; BDUSS_BFESS=lpMkdQRHRaOWxSRUQ5UnBmNy11RTdabi1ab0Y0cjZPN2Z3SjY5b1ZsdEV2RmRqRVFBQUFBJCQAAAAAAAAAAAEAAAD15IanYTEzMTc5MzQyMTcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEQvMGNELzBjcX; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDSFRCVID=TstOJeC62AYxpnTjmKQsMt89F2l-BRRTH6ao89et6MAAoQqyNS1KEG0PBM8g0KAMQgRUogKKQeOTHAkF_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF=tbKJ_CIXtC83fP36q4Q2MtKe22T22jnn-5n9aJ5nJDoNotnxhlO8hfPuKPcJqTcltDtL5fo4QpP-HJA9etoMjxuFLfnIbRcwLb6iKl0MLpoYbb0xyUQY0t-w3fnMBMnI5mOnapjo3fAKftnOM46JehL3346-35543bRTLnLy5KJtMDcnK4-Xj6o3ea7P; BAIDUID_BFESS=3505364E871DBCF31D5A705FC4E1E125:FG=1; BDSFRCVID_BFESS=TstOJeC62AYxpnTjmKQsMt89F2l-BRRTH6ao89et6MAAoQqyNS1KEG0PBM8g0KAMQgRUogKKQeOTHAkF_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF_BFESS=tbKJ_CIXtC83fP36q4Q2MtKe22T22jnn-5n9aJ5nJDoNotnxhlO8hfPuKPcJqTcltDtL5fo4QpP-HJA9etoMjxuFLfnIbRcwLb6iKl0MLpoYbb0xyUQY0t-w3fnMBMnI5mOnapjo3fAKftnOM46JehL3346-35543bRTLnLy5KJtMDcnK4-Xj6o3ea7P; delPer=0; BD_CK_SAM=1; BA_HECTOR=8g2l0084ag0galag25a084h61hqgg6m1j; BDRCVFR[feWj1Vr5u3D]=mk3SLVN4HKm; H_WISE_SIDS=188748_204906_209307_211986_213042_213355_214797_215730_216839_219943_219946_222216_222624_223064_224267_226628_227870_227932_228650_229154_229812_229968_230175_230930_231979_232249_232356_232403_232777_233836_234044_234050_234295_234426_234722_234769_234815_234927_235174_235200_235373_235443_235473_235512_235979_236237_236242_236433_236517_236537_236615_236653_236811_237240_237446_237819_237837_237964_238148_238226_238266_238410_238506_238510_238565_238630_238756_239005_239007_239101_239145_239281_239605_239706_239760_239947_240016_240036_240103_240225_240305_240395_240447_240465_240597_240649_240782_240889_240937_241044_241153_241178_241207_241232_241249_241296_241347; H_WISE_SIDS_BFESS=188748_204906_209307_211986_213042_213355_214797_215730_216839_219943_219946_222216_222624_223064_224267_226628_227870_227932_228650_229154_229812_229968_230175_230930_231979_232249_232356_232403_232777_233836_234044_234050_234295_234426_234722_234769_234815_234927_235174_235200_235373_235443_235473_235512_235979_236237_236242_236433_236517_236537_236615_236653_236811_237240_237446_237819_237837_237964_238148_238226_238266_238410_238506_238510_238565_238630_238756_239005_239007_239101_239145_239281_239605_239706_239760_239947_240016_240036_240103_240225_240305_240395_240447_240465_240597_240649_240782_240889_240937_241044_241153_241178_241207_241232_241249_241296_241347; SE_LAUNCH=5:1672019516; BDPASSGATE=IlPT2AEptyoA_yiU4VKY3kIN8efRNLm4Aeu0S6plBVW4fCWWmhH3BrUzWz0HSieXBDP6wZTXdMsDxXTqXlVXa_EqnBsZolpOaSaXzKGoucHtVM69-t5yILXoHUE2sA8PbRhL-3MEF32EMWosyBDxhvwPisqJyeRhmfr55EDHiMzcGICoYHn2zIKYNnRmOHfEK2328wXxd5NPMVCCROLVLj87hCM9QJ1L70aOatY6C3DzyEQ4Bw4aYfYDCnXd38t13Ai7GwaLxKSl2yU5q-2YSkgtbUbj-_faO5MMAavxlMREN0DtT_H0Li8uKqcmwge; PSINO=2; H_PS_PSSID=37781_36542_37975_37645_37556_37520_37689_37908_36804_37948_37938_37901_26350_37959_37790_37881; H_PS_645EC=c19drKZI2PENKAep9kz4lZvwoZ3t3S65ZFjwutarswMqgR2s8gHnyyI0cFeLF2ecY5Wp'
                }
                # 浏览器取到数据
                resp = requests.get(url=url, headers=headers)
                resp.encoding = 'utf-8'
                # 转为html数据
                needDeal_html = resp.text
                # BS4爬取网页数据
                soup = bs4.BeautifulSoup(needDeal_html, 'html.parser')
                # 获取到div数据块
                divneed = soup.find("div", class_="_aladdin_13t8f_1 ms-epidemic-exp-san_6pupP group_5Cqz4")
                # 字符串拼接取到注释的   疫情搜索比例和 健康指数
                aa = str(divneed).split("s-data:")
                cc = aa[1].split("-->")
                # str 转为json
                jsonData = json.loads(cc[0])
                # 整理数据
                data_list = []
                data_list_needDeal = jsonData["trendData"]["dayData"]["xAxisData"]
                for i in data_list_needDeal:
                    data_list.append("2022" + i.replace(".", ""))
                health_data = jsonData["trendData"]["dayData"]["seriesDatas"][0]
                search_data = jsonData["trendData"]["dayData"]["seriesDatas"][1]
                title_excel = jsonData["title"]
                to_Excel(data_list, search_data, health_data, title_excel, epidemic_data_file_location)
            except Exception as reason:
                problem_list.append(cityname)
                print(cityname, reason)
        except Exception as why:
            print(why)
    return problem_list

if __name__ == '__main__':

    # list = spider_city()
    # print(list)
    list =['山东省莱芜疫情', '山东省泰安疫情', '山东省威海疫情', '山东省日照疫情', '山东省临沂疫情', '山东省滨州疫情', '河南省周口疫情', '河南省黄石疫情', '湖北省鄂州疫情', ' 湖北省随州疫情', ' 湖北省天门疫情', ' 湖北省株洲疫情', '湖南省邵阳疫情', '湖南省永州疫情', '湖南省怀化疫情', '广东省珠海疫情', '广东省汕头疫情', '广东省佛山疫情', '广东省湛江疫情', '广东省茂名疫情', '广东省肇庆疫情', '清远', '济源', '揭阳', '南宁', '柳州', '桂林', '北海', '贵港', '贺州', '河池', '来宾', '崇左', '海口', '三亚', '三亚', '五指山', '万宁', '东方', '成都', '攀枝花', '德阳', '绵阳', '广元', '内江', '乐山', '南充', '眉山', '雅安', '巴中', '资阳', '遵义', '安顺', '昆明', '曲靖', '玉溪', '保山', '昭通', '临沧', '拉萨', '西安', '宝鸡', '延安', '兰州', '金昌', '武威', '张掖', '平凉', '定西', '固原', '中卫', '克拉玛依', '石河子', '北屯', '铁门关', '双河', '可克达拉', '昆玉', '恩施土家族苗族自治州', '延边朝鲜族自治州', '神农架林区', '湘西土家族苗族自治州', '白沙黎族自治县', '乐东黎族自治县', '陵水黎族自治县', '保亭黎族苗族自治县', '琼中黎族苗族自治县', '黔西南布依族苗族自治州', '黔南布依族苗族自治州', '西双版纳傣族自治州', '迪庆藏族自治州', '阿里地区', '临夏回族自治州', '黄南藏族自治州', '果洛藏族自治州', '海西蒙古族藏族自治州', '昌吉回族自治州', '博尔塔拉蒙古自治州', '巴音郭楞蒙古自治州', '克孜勒苏柯尔克孜自治州', '伊犁哈萨克自治州', '和田地区', '塔城地区', '阿勒泰地区', '阿拉善盟']



    print(return_spider(list))





