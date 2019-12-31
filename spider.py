#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/29 16:01
# @Author  : QS
# @File    : spider.py


#潮州空气质量数据采集

import requests
from bs4 import BeautifulSoup
from time import sleep
import datetime
import django
import sys,os
dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE","Pollution_regulation.settings")
django.setup()

from app.models import *

baseUrl = "http://www.tianqihoubao.com"


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
}

def getUrl():
    res = requests.get(url="http://www.tianqihoubao.com/aqi/chaozhou-201911.html",headers=headers).text
    soup = BeautifulSoup(res,"html.parser")
    result = soup.find("div",class_="box").find("ul")
    urls = []
    for i in result.findAll("li"):

        urls.append(baseUrl+i.a['href'])
    urls.reverse()

    return urls

def getInfo(url):
    response = requests.get(url=url,headers=headers).text
    # print(response)
    soup = BeautifulSoup(response,'html.parser')
    trs = soup.findAll("tr")
    flag = True
    data = []
    for i in trs:
        if flag:
            flag = False
            continue
        tds = i.findAll("td")
        date = tds[0].text.strip()
        level = tds[1].text.strip()
        AQI = tds[2].text.strip()
        PM25 = tds[4].text.strip()
        PM10 = tds[5].text.strip()
        SO2 = tds[6].text.strip()
        NO2 = tds[7].text.strip()
        CO = tds[8].text.strip()
        O3 = tds[9].text.strip()

        dateTime_p = datetime.datetime.strptime(date,'%Y-%m-%d')
        if Airquality.objects.filter(date=dateTime_p):
            continue
        print(date)
        Airquality.objects.create(date=dateTime_p,qualityLevel=level,AQI=AQI,PM25=PM25,PM10=PM10,SO2=SO2,NO2=NO2,
                      CO=CO,O3=O3).save()
        # data.append([date,level,AQI,PM10,PM25,SO2,NO2,CO,O3])
    # print(data)
# getInfo(33)


def main():
    urls = getUrl()
    for url in urls:
        print(url)
        getInfo(url)
        sleep(2)


# main()
