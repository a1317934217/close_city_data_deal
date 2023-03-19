# coding:utf-8
"""
@file: test.py
@author: wu hao
@time: 2023/1/14 19:04
@env: 封城数据处理
@desc:
@ref:
"""
import csv
import datetime
import json
import os
import re

import requests
import xlwt
import sys
import urllib.request
import io
import bs4
import time

#数据爬取后的位置
from tqdm import tqdm

def return_spider(list):
    problem_list=[]
    for cityname in list:
        try:
            # 全国31个省市的疫情搜索比例
            # url = 'https://events.baidu.com/api/ncov/indexlist?callback=jsonp_1671962219776_90684'

            # 其余城市的疫情搜索指数
            # url = "https://www.baidu.com/s?sa=re_1_51677&wd={}&rsv_pq=9cf860e800136735&oq=疫情搜索指数&rsv_t=299bc/M9vO7tiAqmufnhJCQgK1H+V2+f9BQxMZeDvjyNvjSuBgGSPzqfpMgdi9uDOLMZ&tn=baiduhome_pg&ie=utf-8".format(cityname)
            url ="https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd={}oq=%25E7%2596%25AB%25E6%2583%2585%25E6%2590%259C%25E7%25B4%25A2%25E6%258C%2587%25E6%2595%25B0&rsv_pq=e0dd1a2000325081&rsv_t=6b75lXgvPzqWMlpA5hACP4g6AONZ3Y6PsioyXK%2BH1q2BgpRdSkwicFo%2FacE&rqlang=cn&rsv_enter=1&rsv_dl=tb&rsv_sug3=39&rsv_sug1=23&rsv_sug7=101&bs=%E7%96%AB%E6%83%85%E6%90%9C%E7%B4%A2%E6%8C%87%E6%95%B0".format(cityname)
            # url = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd={}疫情指数&oq=%25E6%25B8%2585%25E8%25BF%259C%25E7%2596%25AB%25E6%2583%2585%25E6%258C%2587%25E6%2595%25B0&rsv_pq=d51175fe003df102&rsv_t=4564lPPFpjBvzf58Bs%2FTbOKPKLm3SWAStBFxFiIdOD28DHldvDbwaU1vPwg&rqlang=cn&rsv_dl=tb&rsv_enter=1&rsv_n=2&rsv_sug3=26&rsv_sug1=23&rsv_sug7=100&rsv_sug2=0&rsv_btype=t&inputT=7873&rsv_sug4=7873".format(cityname)

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
                divneed = soup.find("div", class_="_aladdin_o4ypw_1 ms-epidemic-exp-san_6pupP group_6pupP")
                # 字符串拼接取到注释的   疫情搜索比例和 健康指数
                aa = str(divneed).split("s-data:")
                cc = aa[1].split("-->")
                # str 转为json
                jsonData = json.loads(cc[0])
                # 整理数据
                data_list = []
                data_list_needDeal = jsonData["trendData"]["dayData"]["xAxisData"]
                localtime = time.localtime(time.time())
                year_current = localtime[0]
                for i in data_list_needDeal:
                    # 这里是处理跨年份的年份问题
                    if i[:2] == "12":
                        data_list.append("2022" + i.replace(".", ""))
                    else:
                        data_list.append(year_current + i.replace(".", ""))
                health_data = jsonData["trendData"]["dayData"]["seriesDatas"][0]
                search_data = jsonData["trendData"]["dayData"]["seriesDatas"][1]
                title_excel = jsonData["title"]

            except Exception as reason:
                problem_list.append(cityname)
                print(cityname, reason)
        except Exception as why:
            print(why)
    return problem_list
list =['上海市疫情指数', '临沧市疫情指数', '丽江市疫情指数', '保山市疫情指数', '大理白族自治州疫情指数', '德宏傣族景颇族自治州疫情指数', '怒江傈僳族自治州疫情指数', '文山壮族苗族自治州疫情指数', '昆明市疫情指数', '昭通市疫情指数', '普洱市疫情指数', '曲靖市疫情指数', '楚雄彝族自治州疫情指数', '玉溪市疫情指数', '红河哈尼族彝族自治州疫情指数', '乌兰察布市疫情指数', '乌海市疫情指数', '兴安盟疫情指数', '包头市疫情指数', '呼伦贝尔市疫情指数', '呼和浩特市疫情指数', '巴彦淖尔市疫情指数', '赤峰市疫情指数', '通辽市疫情指数', '鄂尔多斯市疫情指数', '锡林郭勒盟疫情指数', '北京市疫情指数', '四平市疫情指数', '松原市疫情指数', '白城市疫情指数', '白山市疫情指数', '辽源市疫情指数', '通化市疫情指数', '长春市疫情指数', '吉林省疫情指数', '乐山市疫情指数', '内江市疫情指数', '凉山彝族自治州疫情指数', '南充市疫情指数', '宜宾市疫情指数', '巴中市疫情指数', '广元市疫情指数', '广安市疫情指数', '德阳市疫情指数', '成都市疫情指数', '攀枝花市疫情指数', '泸州市疫情指数', '甘孜藏族自治州疫情指数', '眉山市疫情指数', '绵阳市疫情指数', '自贡市疫情指数', '资阳市疫情指数', '达州市疫情指数', '遂宁市疫情指数', '阿坝藏族羌族自治州疫情指数', '雅安市疫情指数', '天津市疫情指数', '中卫市疫情指数', '吴忠市疫情指数', '固原市疫情指数', '石嘴山市疫情指数', '银川市疫情指数', '亳州市疫情指数', '六安市疫情指数', '合肥市疫情指数', '安庆市疫情指数', '宣城市疫情指数', '宿州市疫情指数', '池州市疫情指数', '淮北市疫情指数', '淮南市疫情指数', '滁州市疫情指数', '芜湖市疫情指数', '蚌埠市疫情指数', '铜陵市疫情指数', '阜阳市疫情指数', '马鞍山市疫情指数', '黄山市疫情指数', '东营市疫情指数', '临沂市疫情指数', '威海市疫情指数', '德州市疫情指数', '日照市疫情指数', '枣庄市疫情指数', '泰安市疫情指数', '济南市疫情指数', '济宁市疫情指数', '淄博市疫情指数', '滨州市疫情指数', '潍坊市疫情指数', '烟台市疫情指数', '聊城市疫情指数', '菏泽市疫情指数', '青岛市疫情指数', '临汾市疫情指数', '吕梁市疫情指数', '大同市疫情指数', '太原市疫情指数', '忻州市疫情指数', '晋中市疫情指数', '晋城市疫情指数', '朔州市疫情指数', '运城市疫情指数', '长治市疫情指数', '阳泉市疫情指数', '东莞市疫情指数', '中山市疫情指数', '云浮市疫情指数', '佛山市疫情指数', '广州市疫情指数', '惠州市疫情指数', '揭阳市疫情指数', '梅州市疫情指数', '汕头市疫情指数', '汕尾市疫情指数', '江门市疫情指数', '河源市疫情指数', '深圳市疫情指数', '清远市疫情指数', '湛江市疫情指数', '潮州市疫情指数', '珠海市疫情指数', '肇庆市疫情指数', '茂名市疫情指数', '阳江市疫情指数', '韶关市疫情指数', '北海市疫情指数', '南宁市疫情指数', '崇左市疫情指数', '来宾市疫情指数', '柳州市疫情指数', '桂林市疫情指数', '梧州市疫情指数', '河池市疫情指数', '玉林市疫情指数', '百色市疫情指数', '贵港市疫情指数', '贺州市疫情指数', '钦州市疫情指数', '防城港市疫情指数', '哈密疫情指数', '乌鲁木齐市疫情指数', '五家渠市疫情指数', '吐鲁番市疫情指数', '喀什地区疫情指数', '图木舒克市疫情指数', '阿克苏地区疫情指数', '阿勒泰地区疫情指数', '阿拉尔市疫情指数', '南京市疫情指数', '南通市疫情指数', '宿迁市疫情指数', '常州市疫情指数', '徐州市疫情指数', '扬州市疫情指数', '无锡市疫情指数', '泰州市疫情指数', '淮安市疫情指数', '盐城市疫情指数', '苏州市疫情指数', '连云港市疫情指数', '镇江市疫情指数', '上饶市疫情指数', '九江市疫情指数', '南昌市疫情指数', '吉安市疫情指数', '宜春市疫情指数', '抚州市疫情指数', '新余市疫情指数', '景德镇市疫情指数', '萍乡市疫情指数', '赣州市疫情指数', '鹰潭市疫情指数', '保定市疫情指数', '唐山市疫情指数', '廊坊市疫情指数', '张家口市疫情指数', '承德市疫情指数', '沧州市疫情指数', '石家庄市疫情指数', '秦皇岛市疫情指数', '衡水市疫情指数', '邢台市疫情指数', '邯郸市疫情指数', '三门峡市疫情指数', '信阳市疫情指数', '南阳市疫情指数', '周口市疫情指数', '商丘市疫情指数', '安阳市疫情指数', '平顶山市疫情指数', '开封市疫情指数', '新乡市疫情指数', '洛阳市疫情指数', '济源市疫情指数', '漯河市疫情指数', '濮阳市疫情指数', '焦作市疫情指数', '许昌市疫情指数', '郑州市疫情指数', '驻马店市疫情指数', '鹤壁市疫情指数', '丽水市疫情指数', '台州市疫情指数', '嘉兴市疫情指数', '宁波市疫情指数', '杭州市疫情指数', '温州市疫情指数', '湖州市疫情指数', '绍兴市疫情指数', '舟山市疫情指数', '衢州市疫情指数', '金华市疫情指数', '浙江省疫情指数', '万宁市疫情指数', '三亚市疫情指数', '东方市疫情指数', '临高县疫情指数', '五指山市疫情指数', '儋州市疫情指数', '定安县疫情指数', '屯昌县疫情指数', '文昌市疫情指数', '昌江黎族自治县疫情指数', '海口市疫情指数', '澄迈县疫情指数', '琼海市疫情指数', '仙桃市疫情指数', '十堰市疫情指数', '咸宁市疫情指数', '天门市疫情指数', '孝感市疫情指数', '宜昌市疫情指数', '武汉市疫情指数', '潜江市疫情指数', '荆州市疫情指数', '荆门市疫情指数', '襄阳市疫情指数', '鄂州市疫情指数', '随州市疫情指数', '黄冈市疫情指数', '黄石市疫情指数', '娄底市疫情指数', '岳阳市疫情指数', '常德市疫情指数', '张家界市疫情指数', '怀化市疫情指数', '株洲市疫情指数', '永州市疫情指数', '湘潭市疫情指数', '益阳市疫情指数', '衡阳市疫情指数', '邵阳市疫情指数', '郴州市疫情指数', '长沙市疫情指数', '兰州市疫情指数', '嘉峪关市疫情指数', '天水市疫情指数', '定西市疫情指数', '平凉市疫情指数', '庆阳市疫情指数', '张掖市疫情指数', '武威市疫情指数', '甘南藏族自治州疫情指数', '白银市疫情指数', '酒泉市疫情指数', '金昌市疫情指数', '陇南市疫情指数', '三明市疫情指数', '南平市疫情指数', '厦门市疫情指数', '宁德市疫情指数', '泉州市疫情指数', '漳州市疫情指数', '福州市疫情指数', '莆田市疫情指数', '龙岩市疫情指数', '山南疫情指数', '日喀则疫情指数', '那曲疫情指数', '拉萨市疫情指数', '昌都市疫情指数', '林芝市疫情指数', '六盘水市疫情指数', '安顺市疫情指数', '毕节市疫情指数', '贵阳市疫情指数', '遵义市疫情指数', '铜仁市疫情指数', '黔东南苗族侗族自治州疫情指数', '丹东市疫情指数', '大连市疫情指数', '抚顺市疫情指数', '朝阳市疫情指数', '本溪市疫情指数', '沈阳市疫情指数', '盘锦市疫情指数', '营口市疫情指数', '葫芦岛市疫情指数', '辽阳市疫情指数', '铁岭市疫情指数', '锦州市疫情指数', '阜新市疫情指数', '鞍山市疫情指数', '重庆市疫情指数', '咸阳市疫情指数', '商洛市疫情指数', '安康市疫情指数', '宝鸡市疫情指数', '延安市疫情指数', '榆林市疫情指数', '汉中市疫情指数', '渭南市疫情指数', '西安市疫情指数', '铜川市疫情指数', '海东市疫情指数', '海北藏族自治州疫情指数', '海南藏族自治州疫情指数', '玉树藏族自治州疫情指数', '西宁市疫情指数', '黄南藏族自治州疫情指数', '七台河市疫情指数', '伊春市疫情指数', '佳木斯市疫情指数', '双鸭山市疫情指数', '哈尔滨市疫情指数', '大兴安岭地区疫情指数', '大庆市疫情指数', '牡丹江市疫情指数', '绥化市疫情指数', '鸡西市疫情指数', '鹤岗市疫情指数', '黑河市疫情指数', '齐齐哈尔市疫情指数']


# 全国31个省市的疫情搜索比例
# url = 'https://events.baidu.com/api/ncov/indexlist?callback=jsonp_1671962219776_90684'

# 其余城市的疫情搜索指数
# url = "https://www.baidu.com/s?sa=re_1_51677&wd={}&rsv_pq=9cf860e800136735&oq=疫情搜索指数&rsv_t=299bc/M9vO7tiAqmufnhJCQgK1H+V2+f9BQxMZeDvjyNvjSuBgGSPzqfpMgdi9uDOLMZ&tn=baiduhome_pg&ie=utf-8".format(cityname)
url = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=北京市疫情&oq=%25E5%258C%2597%25E4%25BA%25AC%25E5%25B8%2582%25E7%2596%25AB%25E6%2583%2585oq%253D%2526lt%253B%2526gt%253B7%2526lt%253B96%2526lt%253BAB%2526lt%253B%2526gt%253B6%2526lt%253B8%2526lt%253B%2526lt%253B85%2526lt%253B%2526gt%253B6%2526lt%253B90%2526lt%253B9%2526lt%253B%2526lt%253B%2526gt%253B7%2526lt%253BB4%2526lt%253BA2%2526lt%253B%2526gt%253B6%2526lt%253B8%2526lt%253B%2526lt%253B87%2526lt%253B%2526gt%253B6%2526lt%253B95%2526lt%253BB0&rsv_pq=9d2258620003a1b5&rsv_t=7785PfnlBxPtHoQJ5VS6by%2BFlJt235%2B8IMz7Zt562y2rpbANX032%2BBCLBMY&rqlang=cn&rsv_dl=tb&rsv_enter=1&rsv_sug3=20&rsv_sug1=7&rsv_sug7=101&rsv_sug2=0&rsv_btype=t&inputT=3423&rsv_sug4=3559"
# url = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd={}疫情指数&oq=%25E6%25B8%2585%25E8%25BF%259C%25E7%2596%25AB%25E6%2583%2585%25E6%258C%2587%25E6%2595%25B0&rsv_pq=d51175fe003df102&rsv_t=4564lPPFpjBvzf58Bs%2FTbOKPKLm3SWAStBFxFiIdOD28DHldvDbwaU1vPwg&rqlang=cn&rsv_dl=tb&rsv_enter=1&rsv_n=2&rsv_sug3=26&rsv_sug1=23&rsv_sug7=100&rsv_sug2=0&rsv_btype=t&inputT=7873&rsv_sug4=7873".format(cityname)
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Cookie': 'BIDUPSID=3505364E871DBCF319777DA02E402DAD; PSTM=1664017249; BAIDUID=3505364E871DBCF31D5A705FC4E1E125:FG=1; BD_UPN=12314753; BDUSS=lpMkdQRHRaOWxSRUQ5UnBmNy11RTdabi1ab0Y0cjZPN2Z3SjY5b1ZsdEV2RmRqRVFBQUFBJCQAAAAAAAAAAAEAAAD15IanYTEzMTc5MzQyMTcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEQvMGNELzBjcX; BDUSS_BFESS=lpMkdQRHRaOWxSRUQ5UnBmNy11RTdabi1ab0Y0cjZPN2Z3SjY5b1ZsdEV2RmRqRVFBQUFBJCQAAAAAAAAAAAEAAAD15IanYTEzMTc5MzQyMTcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEQvMGNELzBjcX; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDSFRCVID=TstOJeC62AYxpnTjmKQsMt89F2l-BRRTH6ao89et6MAAoQqyNS1KEG0PBM8g0KAMQgRUogKKQeOTHAkF_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF=tbKJ_CIXtC83fP36q4Q2MtKe22T22jnn-5n9aJ5nJDoNotnxhlO8hfPuKPcJqTcltDtL5fo4QpP-HJA9etoMjxuFLfnIbRcwLb6iKl0MLpoYbb0xyUQY0t-w3fnMBMnI5mOnapjo3fAKftnOM46JehL3346-35543bRTLnLy5KJtMDcnK4-Xj6o3ea7P; BAIDUID_BFESS=3505364E871DBCF31D5A705FC4E1E125:FG=1; BDSFRCVID_BFESS=TstOJeC62AYxpnTjmKQsMt89F2l-BRRTH6ao89et6MAAoQqyNS1KEG0PBM8g0KAMQgRUogKKQeOTHAkF_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF_BFESS=tbKJ_CIXtC83fP36q4Q2MtKe22T22jnn-5n9aJ5nJDoNotnxhlO8hfPuKPcJqTcltDtL5fo4QpP-HJA9etoMjxuFLfnIbRcwLb6iKl0MLpoYbb0xyUQY0t-w3fnMBMnI5mOnapjo3fAKftnOM46JehL3346-35543bRTLnLy5KJtMDcnK4-Xj6o3ea7P; delPer=0; BD_CK_SAM=1; BA_HECTOR=8g2l0084ag0galag25a084h61hqgg6m1j; BDRCVFR[feWj1Vr5u3D]=mk3SLVN4HKm; H_WISE_SIDS=188748_204906_209307_211986_213042_213355_214797_215730_216839_219943_219946_222216_222624_223064_224267_226628_227870_227932_228650_229154_229812_229968_230175_230930_231979_232249_232356_232403_232777_233836_234044_234050_234295_234426_234722_234769_234815_234927_235174_235200_235373_235443_235473_235512_235979_236237_236242_236433_236517_236537_236615_236653_236811_237240_237446_237819_237837_237964_238148_238226_238266_238410_238506_238510_238565_238630_238756_239005_239007_239101_239145_239281_239605_239706_239760_239947_240016_240036_240103_240225_240305_240395_240447_240465_240597_240649_240782_240889_240937_241044_241153_241178_241207_241232_241249_241296_241347; H_WISE_SIDS_BFESS=188748_204906_209307_211986_213042_213355_214797_215730_216839_219943_219946_222216_222624_223064_224267_226628_227870_227932_228650_229154_229812_229968_230175_230930_231979_232249_232356_232403_232777_233836_234044_234050_234295_234426_234722_234769_234815_234927_235174_235200_235373_235443_235473_235512_235979_236237_236242_236433_236517_236537_236615_236653_236811_237240_237446_237819_237837_237964_238148_238226_238266_238410_238506_238510_238565_238630_238756_239005_239007_239101_239145_239281_239605_239706_239760_239947_240016_240036_240103_240225_240305_240395_240447_240465_240597_240649_240782_240889_240937_241044_241153_241178_241207_241232_241249_241296_241347; SE_LAUNCH=5:1672019516; BDPASSGATE=IlPT2AEptyoA_yiU4VKY3kIN8efRNLm4Aeu0S6plBVW4fCWWmhH3BrUzWz0HSieXBDP6wZTXdMsDxXTqXlVXa_EqnBsZolpOaSaXzKGoucHtVM69-t5yILXoHUE2sA8PbRhL-3MEF32EMWosyBDxhvwPisqJyeRhmfr55EDHiMzcGICoYHn2zIKYNnRmOHfEK2328wXxd5NPMVCCROLVLj87hCM9QJ1L70aOatY6C3DzyEQ4Bw4aYfYDCnXd38t13Ai7GwaLxKSl2yU5q-2YSkgtbUbj-_faO5MMAavxlMREN0DtT_H0Li8uKqcmwge; PSINO=2; H_PS_PSSID=37781_36542_37975_37645_37556_37520_37689_37908_36804_37948_37938_37901_26350_37959_37790_37881; H_PS_645EC=c19drKZI2PENKAep9kz4lZvwoZ3t3S65ZFjwutarswMqgR2s8gHnyyI0cFeLF2ecY5Wp'
}

# # 整理数据
# data_list = []
# data_list_needDeal = jsonData["trendData"]["dayData"]["xAxisData"]
# localtime = time.localtime(time.time())
# year_current = localtime[0]
# for i in data_list_needDeal:
#     # 这里是处理跨年份的年份问题
#     if i[:2] == "12":
#         data_list.append("2022" + i.replace(".", ""))
#     else:
#         data_list.append(year_current + i.replace(".", ""))
# health_data = jsonData["trendData"]["dayData"]["seriesDatas"][0]
# search_data = jsonData["trendData"]["dayData"]["seriesDatas"][1]
list = ['昆明市疫情指数', '红河哈尼族彝族自治州疫情指数', '兴安盟疫情指数', '呼和浩特市疫情指数', '巴彦淖尔市疫情指数', '通辽市疫情指数', '鄂尔多斯市疫情指数', '锡林郭勒盟疫情指数',
        '白城市疫情指数', '白山市疫情指数', '辽源市疫情指数', '通化市疫情指数', '乐山市疫情指数', '内江市疫情指数', '凉山彝族自治州疫情指数', '南充市疫情指数', '宜宾市疫情指数',
        '巴中市疫情指数', '广安市疫情指数', '德阳市疫情指数', '攀枝花市疫情指数', '泸州市疫情指数', '甘孜藏族自治州疫情指数', '眉山市疫情指数', '绵阳市疫情指数', '自贡市疫情指数',
        '资阳市疫情指数', '遂宁市疫情指数', '天津市疫情指数', '吴忠市疫情指数', '固原市疫情指数', '石嘴山市疫情指数', '亳州市疫情指数', '六安市疫情指数', '合肥市疫情指数', '宣城市疫情指数',
        '池州市疫情指数', '淮北市疫情指数', '滁州市疫情指数', '马鞍山市疫情指数', '黄山市疫情指数', '临沂市疫情指数', '威海市疫情指数', '枣庄市疫情指数', '滨州市疫情指数', '潍坊市疫情指数',
        '聊城市疫情指数', '菏泽市疫情指数', '临汾市疫情指数', '吕梁市疫情指数', '大同市疫情指数', '晋中市疫情指数', '晋城市疫情指数', '朔州市疫情指数', '运城市疫情指数', '长治市疫情指数',
        '阳泉市疫情指数', '东莞市疫情指数', '佛山市疫情指数', '惠州市疫情指数', '梅州市疫情指数', '江门市疫情指数', '清远市疫情指数', '肇庆市疫情指数', '阳江市疫情指数', '韶关市疫情指数',
        '北海市疫情指数', '南宁市疫情指数', '崇左市疫情指数', '柳州市疫情指数', '梧州市疫情指数', '河池市疫情指数', '玉林市疫情指数', '百色市疫情指数', '贵港市疫情指数', '贺州市疫情指数',
        '哈密疫情指数', '五家渠市疫情指数', '吐鲁番市疫情指数', '喀什地区疫情指数', '图木舒克市疫情指数', '阿克苏地区疫情指数', '阿勒泰地区疫情指数', '阿拉尔市疫情指数', '南通市疫情指数',
        '泰州市疫情指数', '盐城市疫情指数', '镇江市疫情指数', '九江市疫情指数', '吉安市疫情指数', '宜春市疫情指数', '抚州市疫情指数', '新余市疫情指数', '景德镇市疫情指数', '赣州市疫情指数',
        '鹰潭市疫情指数', '唐山市疫情指数', '承德市疫情指数', '衡水市疫情指数', '邯郸市疫情指数', '信阳市疫情指数', '南阳市疫情指数', '商丘市疫情指数', '平顶山市疫情指数', '开封市疫情指数',
        '新乡市疫情指数', '洛阳市疫情指数', '济源市疫情指数', '许昌市疫情指数', '驻马店市疫情指数', '台州市疫情指数', '嘉兴市疫情指数', '金华市疫情指数', '万宁市疫情指数', '东方市疫情指数',
        '临高县疫情指数', '五指山市疫情指数', '儋州市疫情指数', '定安县疫情指数', '屯昌县疫情指数', '昌江黎族自治县疫情指数', '澄迈县疫情指数', '仙桃市疫情指数', '天门市疫情指数',
        '宜昌市疫情指数', '潜江市疫情指数', '荆州市疫情指数', '荆门市疫情指数', '鄂州市疫情指数', '黄冈市疫情指数', '娄底市疫情指数', '岳阳市疫情指数', '张家界市疫情指数', '永州市疫情指数',
        '湘潭市疫情指数', '益阳市疫情指数', '衡阳市疫情指数', '郴州市疫情指数', '长沙市疫情指数', '兰州市疫情指数', '嘉峪关市疫情指数', '天水市疫情指数', '定西市疫情指数', '平凉市疫情指数',
        '张掖市疫情指数', '武威市疫情指数', '甘南藏族自治州疫情指数', '白银市疫情指数', '酒泉市疫情指数', '金昌市疫情指数', '三明市疫情指数', '泉州市疫情指数', '漳州市疫情指数',
        '莆田市疫情指数', '龙岩市疫情指数', '山南疫情指数', '日喀则疫情指数', '那曲疫情指数', '昌都市疫情指数', '林芝市疫情指数', '六盘水市疫情指数', '安顺市疫情指数', '毕节市疫情指数',
        '铜仁市疫情指数', '黔东南苗族侗族自治州疫情指数', '抚顺市疫情指数', '朝阳市疫情指数', '本溪市疫情指数', '沈阳市疫情指数', '盘锦市疫情指数', '辽阳市疫情指数', '重庆市疫情指数',
        '咸阳市疫情指数', '商洛市疫情指数', '安康市疫情指数', '宝鸡市疫情指数', '延安市疫情指数', '铜川市疫情指数', '海东市疫情指数', '海北藏族自治州疫情指数', '海南藏族自治州疫情指数',
        '玉树藏族自治州疫情指数', '西宁市疫情指数', '黄南藏族自治州疫情指数', '七台河市疫情指数', '伊春市疫情指数', '佳木斯市疫情指数', '双鸭山市疫情指数', '大兴安岭地区疫情指数',
        '牡丹江市疫情指数', '绥化市疫情指数', '鸡西市疫情指数', '黑河市疫情指数', '齐齐哈尔市疫情指数']


for i in list:
    print(i[2:])



