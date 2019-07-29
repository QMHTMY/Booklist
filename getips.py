#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#    Author: Shieber
#    Date: 2019.07.23
#
#                             APACHE LICENSE
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
#                            Function Description
#    获取ip，构建代理池
#
#    Copyright 2019 
#    All Rights Reserved!

import re
import urllib
import requests
import random
from bs4 import BeautifulSoup as Soup


def getIpList(url):
    headers  = {
                'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;rv:68.0)\
                Gecko/20100101 Firefox/68.0',
                'Connection':'close'
               } 

    resp = requests.get(url,headers)
    soup = Soup(resp.content,'html.parser')
    
    table = soup.find('table',class_="table table-hover table-bordered")
    tbody = table.find('tbody')
    trs   = tbody.find_all('tr')

    ip_list   = []
    patn = re.compile(r'check.html')
    for tr in trs:
        info = tr.find('a',href=patn)
        if info:
            ip = str(info.getText())
            ip = ip.strip()
            if ip:
                ip_list.append('http://'+ip)

    ip_list = checkip(url,ip_list)
    return ip_list

def checkip(url,ip_list):
    for ip in ip_list:
        try:
            prox = {"https":ip}
            resp = urllib.urlopen(url, proxies=prox).read()
        except Exception as e:
            ip_list.remove(ip)
            continue
    return ip_list

def getRandomIp(ip_list):
    ''' 
        proxies = {https: 'https:192.168.112.54'} 
        proxies = {http: 'https:192.168.112.54'} 
        https和http指要爬取的网站的类型
    '''
    if ip_list:
        proxy_ip = random.choice(ip_list)
        proxies = { 'https': proxy_ip}
        return proxies
    else:
        return None

if __name__ == "__main__":
    url = 'https://ip.ihuan.me/'
    ip_list = getIpList(url)
    proxies = getRandomIp(ip_list)
    print(proxies)
