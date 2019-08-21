#!/usr/bin/python3
# coding: utf-8

import os
import re
import sys
import json
import time
import requests
from bs4 import BeautifulSoup as Soup
from random import randint
from multiprocessing import Pool
from selenium import webdriver

class SocietyNews():
    def __init__(self):
        self.infos    = []          #信息存储，元素为字典
        self.mlsufix  = 'mail.html' #html后缀名
        self.headers  = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) \
             AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Connection':'close'
            }

        self.urls     = {           #将函数和网站绑定，以便于随意安放次序
            'qiushiw' :[self.site13, 'http://english.qstheory.cn',False],
            'zhjiwei' :[self.site10, 'http://www.ccdi.gov.cn/scdc',False],
            'newbook' :[self.site0 , 'https://book.douban.com',False],
            'moviede' :[self.site23, 'https://maoyan.com/board',False],
            'hotsong' :[self.site1 , 'https://music.163.com/discover/toplist',False],
            'egouzweb':[self.site19, 'https://www.egouz.com/world',False], 
            'entrtain':[self.site8 , 'https://ent.sina.com.cn',False],
            'hottrend':[self.site24, 'http://www.vogue.com.cn',False],
            'magzine' :[self.site15, 'https://www.zazhimall.com',False], 
            'perfect' :[self.site12, 'http://www.fsdpp.cn',False], 
            'chinad'  :[self.site20, 'http://language.chinadaily.com.cn/trans_collect',False], 
            'stockmak':[self.site2 , 'http://quotes.money.163.com/stock',False],
            '21centay':[self.site9 , 'http://www.21jingji.com',False],
            'finance' :[self.site5 , 'http://economy.caixin.com',False],
            'company' :[self.site14, 'http://companies.caixin.com',False],
            'technolg':[self.site3 , 'http://tech.feng.com',False],
            'huanqiu' :[self.site22, 'https://www.huanqiukexue.com',False], 
            'jiqizhix':[self.site11, 'https://www.jiqizhixin.com',False], 
            'qbits'   :[self.site17, 'https://www.qbitai.com',False], 
            'medicing':[self.site7 , 'http://www.bioon.com',False],
            'society' :[self.site6 , 'http://news.cctv.com/society',False],
            'polictal':[self.site4 , 'http://www.huanqiu.com',False],
            'people'  :[self.site21, 'http://www.people.com.cn',False], 
            'banyue'  :[self.site16, 'http://www.banyuetan.org',False], 
            }
        #self.setDriver()

    def setDriver(self):
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Firefox()

    def closeDriver(self):
        self.driver.close()

    def readHtml(self, name):
        with open(name) as fobj:
            cnt  = fobj.read()
            soup = Soup(cnt, 'html.parser')
        return soup

    def saveHtml(self, name, resp):
        with open(name, 'w') as fobj:
            fobj.write(str(resp.text))

    def getHtmldriver(self, kind, url, driver):
        try:
            name = kind + '.html' 
            driver.get(url)
            resp = driver.page_source
            with open(name, 'w') as fobj:
                fobj.write(resp)
        except Exception as err:
            pass 
            print(err)

    def getHtml(self, kind, url):
        try:
            name = kind + '.html' 
            resp = requests.get(url, headers=self.headers)
            if 200 == resp.status_code:
                resp.encoding = 'utf-8'
                self.saveHtml(name, resp)
            else:
                print('Failue')
        except Exception as err:
            print(err)

    def getSoup(self, url, driver=False):
        '''获取网页信息'''
        soup = []
        try:
            if driver: #是否开启无头浏览器下载
                self.driver.get(url)
                resp = self.driver
                soup = Soup(resp)
                return soup

            resp = requests.get(url,headers=self.headers)
            if 200 == resp.status_code:
                resp.encoding = 'utf-8'
                soup = Soup(resp.content, 'html.parser')
            return soup
        except Exception as err:
            return soup 

    def site0(self, soup):
        '''豆瓣'''
        div = soup.find('div', attrs={"class":"section books-express"})
        div = div.find('div', attrs={"class":"bd"})
        uls = div.find_all('ul',attrs={"class":"list-col list-col5 list-express slide-item"})

        ul  = uls[randint(0,3)]
        lis = ul.find_all('li')
        li  = lis[randint(0,9)]
        a   = li.find('a')

        url = a['href']
        ttl = '新书：' + a['title']
        img = a.find('img')
        iul = img['src']
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})


    def site1(self, soup):
        '''网易音乐,排行榜数据'''
        def getBang(sp):
            '''获取歌单页soup'''
            div = sp.find('div', attrs={"class":"n-minelst n-minelst-2"})
            uls = div.find_all('ul',attrs={"class":"f-cb"})
            ul  = uls[randint(0,len(uls)-1)]
            
            lis = ul.find_all('li',attrs={"class":"mine"})
            li  = lis[randint(0,len(lis)-1)]
            tul = self.urls['hotsong'][1] + '?id=' + li['data-res-id']
            sp  = self.getSoup(tul)
            return sp

        soup= getBang(soup)
        div = soup.find('div', attrs={"class":"g-mn3c"})

        dv1 = div.find('div', attrs={"class":"g-wrap"}) 
        img = dv1.find('img')
        iul = img['src']
        h2  = dv1.find('h2')
        ttl = str(h2.getText().strip()) + '《'

        ul  = soup.find('ul', attrs={"class":"f-hide"})
        lis = ul.find_all('li')
        li  = lis[randint(0,len(lis)-1)]
        a   = li.find('a')

        url = 'https://music.163.com' + a['href']
        ttl = '音乐：' + ttl + str(a.getText().strip()) + '》'
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site2(self, soup):
        '''网易股市行情'''
        def getStockData():
            idx_urls = [
            ['http://img1.money.126.net/data/hs/time/today/0000001.json','上证指数'],
            ['http://img1.money.126.net/data/hs/time/today/1399001.json','深证成指'],
            ['http://img1.money.126.net/data/hs/time/today/1399006.json','创业板指']
            ]
            tmp = ''
            for iurl in idx_urls:
                resp = requests.get(iurl[0],headers=self.headers)
                jdic = json.loads(resp.content)
                data = jdic['data']
                yst  = jdic['yestclose']
                ops, cur = data[0][1], data[-1][1]
                chg = cur - yst
                pct = round(100*(chg/yst), 2)

                if pct > 0:
                    pct = '+' + str(pct) 
                else:
                    pct = str(pct)
                tmp += '%s：%.2f|%.2f|%.2f|%.2f|%s%%<br>'%(iurl[1], yst, ops, cur, chg, pct)
            return tmp

        div = soup.find('div', attrs={"class":"thumbnails thumbnail-point fetch-content"})
        dvs = div.find_all('div', attrs={"class":"thumbnail ne-template fetch-el"})
        div = div.find('div', attrs={"class":"body"})

        img = div.find('img')
        iul = img['src']
        url = self.urls['stockmak'][1] 
        ttl = '沪深股市行情 [昨收，今开，现值，涨跌，涨跌比]<br>'

        tmp  = getStockData()
        ttl += tmp
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl})

    def site3(self, soup):
        '''威锋'''
        div = soup.find('div', attrs={"class":"techbanner"})
        lis = div.find_all('li')
        li  = lis[randint(0,len(lis)-1)]
        
        img = li.find('img')
        iul = img['src']
        aa  = li.find_all('a')
        a   = aa[1]

        url = a['href']
        ttl = '科技：' + str(a.getText().strip())
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site4(self, soup):
        '''环球'''
        div = soup.find('div', attrs={"id":"foucsBox"}) 
        ul  = div.find('ul', attrs={"id":"imgCon"})
        lis = ul.find_all('li')
        li  = lis[randint(0,len(lis)-1)]
        a   = li.find('a')
        
        url = a['href']
        ttl = '时政：' + a['title']
        img = a.find('img')
        iul = img['src']
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site5(self, soup):
        '''财新网；经济'''
        div = soup.find('div', attrs={"class":"indexMain"})
        div = div.find('div', attrs={"class":"topNews"})
        aa  = div.find_all('a') 

        url = aa[-1]['href']
        ttl = '经济：' + str(aa[-1].getText().strip())
        img = div.find('img')
        iul = img['src']
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site14(self, soup):
        '''财新网；公司'''
        div = soup.find('div', attrs={"class":"indexMain"})
        div = div.find('div', attrs={"class":"topNews"})

        img = div.find('img')
        iul = img['src']

        aa  = div.find_all('a') 
        url = aa[1]['href']
        ttl = '企业：' + str(aa[1].getText().strip())
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})
            
    def site6(self, soup):
        '''央视网，社会'''
        div = soup.find('div', attrs={"class":"content"})
        a   = div.find('a')

        url = a['href']
        ttl = '社会：' + str(a.getText().strip())
        img = div.find('img')
        iul = img['src']
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})
            
    def site7(self, soup):
        '''医药谷'''
        div = soup.find('div', attrs={"class":"index_banner"})
        div = div.find('div', attrs={"class":"fl retv"})
        aa  = div.find_all('a')
        a   = aa[randint(0,len(aa)-1)]

        url = a['href']
        img = a.find('img')
        iul = img['src']
        div = a.find('div')
        ttl = '医疗：' + str(div.getText().strip())
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})
            
    def site8(self, soup):
        '''新浪'''
        div = soup.find('div', attrs={"class":"scroll"})
        a   = div.find('a')

        url = a['href']
        img = div.find('img')
        ttl = '娱乐：' + img['alt']
        iul = 'https:' + img['src']
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site9(self, soup):
        '''21centay'''
        div = soup.find('div', attrs={"id":"wrapper"})
        lis = div.find_all('li')
        li  = lis[randint(0,len(lis)-1)]
        a   = li.find('a')

        url = a['href']
        ttl = '经济：' + a['title']
        img = a.find('img')
        iul = img['src']
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site10(self, soup):
        '''中纪委'''
        div = soup.find('section', attrs={"class":"main fixed"})
        uls = div.find_all('ul',attrs={"class":"list_news_dl fixed"})
        ul  = uls[randint(0,len(uls)-1)]
        lis = ul.find_all('li')
        li  = lis[randint(0,len(lis)-1)]
        a   = li.find('a')

        ttl = '反腐：' + str(a.getText().strip())
        url = self.urls['zhjiwei'][1]
        iul = 'https://s2.ax1x.com/2019/08/20/mYJHSJ.png'
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})


    def site12(self, soup):
        '''perfect idears'''
        ul  = soup.find('ul', attrs={"id":"menu"})
        lis = ul.find_all('li')
        li  = lis[randint(0,len(lis)-2)]
        a   = li.find('a')
        tul = a['href']

        soup = self.getSoup(tul)
        div  = soup.find('div', attrs={"class":"mainbox"})
        dvs  = div.find_all('div', attrs={"class":"post"})
        div  = dvs[randint(0,len(dvs)-1)]
        div  = div.find('div', attrs={"class":"entry-content"})
        a    = div.find('a')

        url  = self.urls['perfect'][1] + a['href']
        img  = a.find('img')
        iul  = img['src']
        ttl  = '奇趣：' + img['alt']
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site13(self, soup):
        '''求是网：习新闻'''
        div = soup.find('div', attrs={"class":"slide"})
        dv1 = div.find('div', attrs={"class":"content-main-visual"})
        aa  = dv1.find_all('a')
        dv2 = div.find('div', attrs={"class":"content-main-feature"})
        dvs = dv2.find_all('div')
        
        num = randint(0,len(aa)-1)
        a   = aa[num]
        div = dvs[num]

        url = a['href']
        img = a.find('img')
        iul = self.urls['qiushiw'][1] + '/' + img['src']
        a   = div.find('a')
        ttl = 'Leader：' + str(a.getText().strip())
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site15(self, soup):
        '''杂志网'''
        tul  = self.urls['magzine'][1] + '/%d'%randint(94,103)
        soup = self.getSoup(tul)
        ul  = soup.find('ul',attrs={"class":"list-grid clearfix"})
        lis = ul.find_all('li')
        li  = lis[randint(0,len(lis)-1)]
        a   = li.find('a')

        url = self.urls['magzine'][1] + a['href']
        ttl = '杂志：' + a['title']
        img = a.find('img')
        iul = img['data-original']
        self.infos.append({'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site16(self, soup):
        '''半月谈'''
        div = soup.find('div', attrs={"bty_tbtj_list js-tbtj"})
        lis = div.find_all('li')
        li  = lis[randint(0,len(lis)-1)]

        img = li.find('img')
        iul = img['src']

        h3  = li.find('h3')
        a   = h3.find('a')
        url = a['href']
        ttl = '时评：' + str(a.getText().strip())
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})


    def site22(self, soup):
        '''环球科学'''
        div = soup.find('div', attrs={"class":"arrang"})
        lis = div.find_all('li')
        li  = lis[randint(0,len(lis)-1)]
        a   = li.find('a')

        url = self.urls['huanqiu'][1] + a['href']
        ttl = '科学：' +str(a.getText().strip())
        img = li.find('img')
        iul = self.urls['huanqiu'][1] +img['src']
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site23(self, soup):
        '''猫眼票房'''
        dl = soup.find('dl', attrs={"class":"board-wrapper"})
        dd = dl.find('dd')
        a  = dd.find('a')

        url = self.urls['moviede'][1] + a['href']
        img = a.find('img', attrs={"class":"board-img"})
        iul = img['data-src']
        ttl = img['alt']

        p   = dd.find('p', attrs={"class":"score"})
        ii  = p.find_all('i')
        scr = ii[0].getText().strip() + ii[1].getText().strip()
        ttl = '电影排行榜<br>' + '影名：%s<br>'%ttl +'评分：' + scr 

        self.infos.append({'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site24(self, soup):
        '''潮流'''
        dvs = soup.find_all('div', attrs={"class":"swiper-container"})
        num = randint(0,len(dvs)-1)
        div = dvs[num]

        if 5 != num and 6 != num:
            aa  = div.find_all('a')
            a   = aa[randint(0,len(aa)-1)]
            url = 'http:' + a['href']
            ttl = '潮流：' + a['title']
            img = a.find('img')
            iul = 'http:' + img['src']
        else:
            lis = div.find_all('li')
            li  = lis[randint(0,len(lis)-1)]
            ttl = '潮流：' + li['data-des']
            a   = li.find('a')

            url = 'http:' + a['href']
            img = a.find('img')
            iul = 'http:' + img['data-original']

        self.infos.append({'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

              
    def site11(self, soup):
        '''机器之心'''
        div = soup.find('div', attrs={"class":"u-block__body home__newest"})
        div = div.find('div', attrs={"class":"u-block__item js-u-item is-active"})
        ars = div.find_all('article')
        arc = ars[randint(0,len(ars)-1)]

        a   = arc.find('a')
        url = self.urls['jiqizhix'][1] + a['href']
        img = a.find('img')
        iul = img['src']
        ttl = '人工智能：' + img['alt']
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site17(self, soup):
        '''量子位'''
        div = soup.find('div', attrs={"class":"article_list"})
        dvs = div.find_all('div', attrs={"class":"picture_text"})
        div = dvs[randint(0,len(dvs)-1)]

        img = div.find('img')
        iul = img['src']

        h4  = div.find('h4')
        a   = h4.find('a')
        url = a['href']
        ttl = '人工智能：' + str(a.getText().strip())
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site18(self, soup):
        '''网站推荐'''
        div  = soup.find('div', attrs={"class":"box-module list-module"})
        div  = div.find('div', attrs={"class":"box-body"})
        li   = div.find('li', attrs={"class":"tab active"})
        lis  = li.find_all('li')
        li   = lis[randint(0,len(lis)-1)]
        a    = li.find('a')

        url  = 'https://www.egouz.com' + a['href']
        img  = a.find('img')
        iul  = 'https://www.egouz.com' + img['src']
        ttl  = img['title']
        ttl  = '网站推荐：'  + img['title'].replaec(':','，') 
        return url, iul, ttl

    def site19(self, soup):
        '''全球网站推荐'''
        dvs = soup.find_all('div', attrs={"class":"country-module"})
        div = dvs[randint(0,len(dvs)-1)]
        div = div.find('div', attrs={"class":"box-body"})
        lis = div.find_all('li')
        li  = lis[randint(0,len(lis)-1)]
        a   = li.find('a')

        tul, img = a['href'], a.find('img')
        cty = img['title']

        soup = self.getSoup(tul)
        div  = soup.find('div', attrs={"class":"page-box"})
        aa   = div.find_all('a')
        page = int(aa[-2].getText().strip())

        tul = a['href'] + '%d.html'%randint(1,page)
        soup = self.getSoup(tul)
        url, iul, ttl = self.site18(soup)
        ttl = cty + ttl
        self.infos.append({'url':url, 'iul':iul, 'ttl':ttl+'<br>'})
        
    def site20(self, soup):
        '''中国日报双语'''
        pag = randint(1,103)
        tul = self.urls['chinad'][1] + '/page_%d.html'%pag
        soup = self.getSoup(tul)
        div = soup.find('div', attrs={"class":"content_left"})
        dvs = div.find_all('div', attrs={"class":"gy_box"})
        div = dvs[randint(0,len(dvs)-1)]
        
        img = div.find('img')
        iul = 'http:' + img['src']

        aa  = div.find_all('a')
        url = 'http:' + aa[1]['href']
        ttl = '英语点津：' + str(aa[1].getText().strip())
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site21(self, soup):
        '''人民日报'''
        div = soup.find('div', attrs={"id":"focus_list"})
        lis = div.find_all('li')
        li  = lis[randint(0,len(lis)-1)]

        img = li.find('img')
        iul = self.urls['people'][1] + img['src']
        aa  = li.find_all('a')
        a   = aa[1]
        url = a['href']
        ttl = '时政：' + str(a.getText().strip())
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def downloadInfos(self):
        for item in self.urls.values():
            try:
                soup = self.getSoup(item[1])
                if not soup:
                    continue
                item[0](soup)           #核心函数
            except Exception as err:
                continue

    def downloadInfosT(self):
        for item in self.urls.values():
            soup = self.getSoup(item[1])
            if not soup:
                continue
            item[0](soup)   

    def multidownloadInfos(self):
        def download(item):
            soup = self.getSoup(item[1])
            if not soup:
                return None
            item[0](soup)

        pool = Pool(10)
        for item in self.urls.values():
            pool.apply_async(download, (item,))
        pool.close()
        pool.join()

    def writeInfo2html(self, name):
        '''提取信息并保存'''
        tim = time.strftime("%b %d, %Y",time.localtime())
        with open(name + self.mlsufix ,'a') as fobj:
            for dic in self.infos:
                url = dic['url']
                iul = dic['iul']
                ttl = dic['ttl'] 
                item = '''<a href="%s" target="_blank"><img src="%s" class="img" width="600" border="0" alt="" style="display: block;"></a> 
<table bgcolor="#111111" width="100%%" cellpadding="20" cellspacing="0" border="0"><tbody><tr><td align="left">
<div style="color: #ffffff; font-family: helvetica, arial, sans-serif; font-size: 12px;"><a href="%s" style="color: #ffffff; font-size: 24px; text-decoration: none;" target="_blank"> %s </a><br>
<a style="color: #cc2016; text-decoration: none;"> Shieber </a> | %s </div>
</td></tr></tbody></table>\n\n'''%(url, iul, url, ttl, tim)
                fobj.write(item)

    def writePreSuf(self, presuf, name, mode):
        with open(presuf) as fobj1:
            cnt = fobj1.read()
            with open(name + self.mlsufix, mode) as fobj:
                fobj.write(cnt)

    def printinfo(self):
        for dic in self.infos:
            print(dic)

if __name__ == "__main__":
    name = 'Societynews'
    pref = 'Societynewspre.html'
    suff = 'Societynewssuf.html'

    spider = SocietyNews()
    #spider.getHtml(kind, url)
    #spider.downloadInfosT()
    spider.downloadInfos()
    #spider.printinfo()

    spider.writePreSuf(pref, name, 'w')
    spider.writeInfo2html(name)
    spider.writePreSuf(suff, name, 'a')

    #options = webdriver.FirefoxOptions()
    #options.add_argument('--headless')
    #options.add_argument("User-Agent='Mozilla/5.0 (Windows NT 6.1; WOW64) \
    #    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'")
    #driver = webdriver.Firefox(firefox_options=options)
    #driver.set_page_load_timeout(10)
    #driver.close()
    #spider.getHtmldriver(kind, url, driver)
    #财经 #奢侈品  #健身    #医疗 
    #政治 #设计    #教育 
    #社会 #旅游    #计算机 
    #歌曲 #推荐    #地震
    #书籍 #美食    #死亡人数 
    #电影 #酒店    #出生人数 
    #股市 #介绍    #总人口数
    #服装 #服务    #科技 
    #汽车 #广告    #电信
    #航天 #健康    #时尚 
