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
        self.infos    = []          
        self.mlsufix  = 'mail.html' 
        self.headers  = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) \
             AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Connection':'close'
            }
        self.urls     = {           
            #'nature'  :[self.site01,'https://www.nature.com',False],
            #'science' :[self.site02,'https://www.sciencemag.org',False],
            #'animalfu':[self.site03,'https://www.animalfactsencyclopedia.com',False],
            #'forbes'  :[self.site04,'https://www.forbes.com',False],
            #'arstech' :[self.site05,'https://arstechnica.com',False],
            #'engadget':[self.site06,'https://www.engadget.com',False],
            #'techcrun':[self.site07,'https://www.techcrunch.com',False],
            #'gizmodo' :[self.site08,'https://gizmodo.com',False],
            #'readwrit':[self.site09,'https://readwrite.com',False],
            #'ventureb':[self.site10,'https://venturebeat.com',False],
            #'lifehack':[self.site11,'https://lifehacker.com',False],
            #'wiredweb':[self.site12,'https://www.wired.com',False],
            #'newyorkr':[self.site13,'https://www.newyorker.com',False],
            #'caranddr':[self.site14,'https://www.caranddriver.com',False],
            #'ideasted':[self.site15,'https://ideas.ted.com',False],
            #'psycholg':[self.site16,'https://www.psychologytoday.com',False],
            #'sunset'  :[self.site17,'https://www.sunset.com',False],
            #'scientif':[self.site18,'https://www.scientificamerican.com',False],
            #'mentalfl':[self.site19,'http://mentalfloss.com',False],
            #'epicurio':[self.site20,'https://www.epicurious.com',False],
            #'aeonweb' :[self.site21,'https://aeon.co',False],
            #'playboym':[self.site22,'https://www.playboy.com',False],
            #'vanityfa':[self.site23,'https://www.vanityfair.com',False],
            #'travelad':[self.site24,'https://www.travelandleisure.com',False],
            #'ciowebsi':[self.site25,'https://www.cio.com',False],
            #'computew':[self.site26,'https://www.computerworld.com',False],
            }

    def saveHtml(self, name, resp):
        with open(name, 'w') as fobj:
            fobj.write(str(resp.text))

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

    def getSoup(self, url):
        '''获取网页信息'''
        soup = []
        try:
            resp = requests.get(url,headers=self.headers)
            if 200 == resp.status_code:
                resp.encoding = 'utf-8'
                soup = Soup(resp.content, 'html.parser')
            return soup
        except Exception as err:
            return soup 

    def site01(self, soup):
        '''nature'''
        a = soup.find('a',attrs={"class":"featured-article"})

        url = a['href']
        img = a.find('img')
        iul = 'https:' + img['src']
        h3  = a.find('h3')
        ttl = 'Nature: ' + str(h3.getText().strip())
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site02(self, soup):
        '''science'''
        ars = soup.find_all('article',attrs={"class":"hero--inset hero--superhero"})
        arc = ars[randint(0,len(ars)-1)]
        a   = arc.find('a')

        url = a['href']
        img = a.find('img')
        iul = 'https:' + img['src']
        h2  = arc.find('h2')
        a   = h2.find('a')
        ttl = str(a.getText().strip())
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site03(self, soup):
        '''xxxx'''
        dvs = soup.find_all('div',attrs={"class":"ImageBlock ImageBlockCenter"})
        div = dvs[randint(0,len(dvs)-1)]

        img = div.find('img')
        iul = img['data-pin-media']
        url = self.urls['animalfu'][1]
        ttl = 'Animal'
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site04(self, soup):
        '''forbes'''
        imp = re.compile(r'url\(.*\)')
        div = soup.find('div',attrs={"class":"card card--large csf-block"})
        a   = div.find('a')

        url = a['href']
        ttl = a['aria-label']
        div = div.find('div',attrs={"class":"preview__image"})
        stl = div['style']
        img = imp.search(stl)
        iul = img.group(1) 
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site05(self, soup):
        '''arstechnica'''
        sec = soup.find('section', attrs={"class": "listing listing-top with-feature"})
        lis = sec.find_all('lis')
        li  = lis[randint(0,len(lis)-1)]
        
        h2  = li.find('h2')
        a   = h2.find('a')
        url = a['href']
        ttl = str(h2.getText().strip())

        imp = re.compile(r"url\('(.*)'\)")
        div = li.find('div',attrs={"class":"listing listing-large"})
        stl = div['style']
        img = imp.search(stl)
        iul = img.group(1)
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site06(self, soup):
        '''engadget'''
        div = soup.find('div',attrs={"id":"engadget-the-latest"})
        dvs = div.find_all('div',attrs={"class":"border-top@m+ mt-40@m+ pt-40@m+"})
        div = dvs[randint(0,len(dvs)-1)]
        
        img = div.find('img')
        url = img['src']
        ttl = img['alt']
        a   = div.find('a',attrs={"class":"o-hit__link"})
        url = self.urls['engadget'][1] +  a['href']
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site07(self, soup):
        '''techcrunch'''
        div = soup.find('div',attrs={"class":"river river--homepage"})
        ars = div.find_all('article',attrs={"class":"post-block post-block--image"})
        arc = ars[randint(0,len(ars)-1)]
        h2  = arc.find('h2')
        a   = h2.find('a')

        url = self.urls['techcrun'][1] + a['href']
        ttl = str(a.getText().strip())
        img = arc.find('img')
        iul = img['src']
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site08(self, soup):
        '''gizmodo'''
        div = soup.find('div',attrs={"sc-17uq8ex-0 keWBE0"})
        ars = div.find_all('article',attrs={"class":"js_post_item cw4lnv-0 gzvDHx"})
        arc = ars[randint(0,len(ars)-1)]
        imp = re.compile(r'(.*)320w, (.*) 470w')

        img = arc.find('img')
        src = img['srcset']
        img = imp.search('img')
        iul = img.group(2)

        a   = arc.find('a',attrs={"class":"js_link sc-lout364-0 fwjlm0"})
        url = a['href']
        h1  = a.find('h1')
        ttl = str(h1.getText().strip())
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site09(self, soup):
        '''readwrite'''
        div = soup.find('div',attrs={"home-posts-wrap"})
        ars = div.find_all('article',attrs={"id":"post-"})
        arc = ars[randint(0,len(ars)-1)]

        img = arc.find('img')
        iul = img['src']

        h2  = arc.find('h2')
        a   = h2.find('a')
        url = a['href']
        ttl = str(a.getText().strip())
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site10(self, soup):
        '''venturebeat'''
        imp = re.compile(r'(.*)\.(.*)g\?')
        div = soup.find('div',attrs={"story-river"})
        ars = div.find_all('id',attrs={"post-"})
        arc = ars[randint(0,len(ars)-1)]

        img = arc.find('img')
        img = img['src']
        img = imp.search(img)
        iul = img.group(1) + '.%sg'%img.group(2)

        h2  = arc.find('h2')
        a   = h2.find('a')
        url = a['href']
        ttl = str(a.getText().strip())
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site11(self, soup):
        '''lifehacker'''
        imp = re.compile(r'(.*)470w, (.*) 800w')
        dvs = soup.find_all('div',attrs={"class":"grid__zone curation-module"})
        div = dvs[randint(0,len(dvs)-1)]
        dvs = div.find_all('div',attrs={"class":"zone__item"})
        div = dvs[randint(0,len(dvs)-1)]
        a   = div.find('a')

        url = a['href']
        ttl = a['title']
        img = a.find('img')
        img = img['srcset']
        img = imp.search(img)
        iul = img.group(2)
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site12(self, soup):
        '''wired'''
        imp = re.compile(r'(.*)225w, (.*) 1000w')
        ul  = soup.find('ul',attrs={"post-listing-component__list"})
        lis = ul.find_all('li')
        li  = lis[randint(0,len(lis)-1)]
        a   = li.find('a')

        url = self.urls['wiredweb'][1] +  a['href']
        h5  = li.find('h5')
        ttl = str(h5.getText().strip())
        img = li.find('img')
        img = imp.search('img')
        iul = img.group(2)
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site13(self, soup):
        '''newyorker'''
        imp = re.compile(r'(.*)\.jpg, (.*)\.jpg 2x')
        #第一条
        div = soup.find('div',attrs={"class":"Card__content___2_jDO undefined"})

        src = div.find('source')
        src = src['srcset']
        img = imp.search(src)
        iul = img.group(2) + '.jpg'

        a   = div.find('a',attrs={"class":"hit__link___3dWao"})
        url = self.urls['newyorkr'][1] +  a['href']
        h3  = a.find('h3')
        ttl = str(h3.getText().strip())
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

        #第二条
        imp = re.compile(r'(.*)\.jpg, (.*)\.jpg 2x')
        div = soup.find('div',attrs={"class":"SpotlightSection__itemsColumn"})
        dvs = div.find_all('div',attrs={"class":"SpotlightSection__spotlightItem"})
        div = dvs[randint(0,len(dvs)-1)]

        src = div.find('source')
        src = src['srcset']
        img = imp.search(src)
        iul = img.group(2) + '.jpg'

        a   = div.find('a',attrs={"class":"hit__link___3dWao"})
        url = self.urls['newyorkr'][1] +  a['href']
        h3  = a.find('h3')
        ttl = str(h3.getText().strip())
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site14(self, soup):
        '''caranddriver'''
        dvs = div.find_all('div',attrs={"class":"feed-block-column feed-block-column"})
        div = dvs[randint(0,len(dvs)-1)]
        dvs = div.find_all('div',attrs={"class":"custom-item"})
        div = dvs[randint(0,len(dvs)-1)]
        a   = div.find('a',attrs={"class":"custom-item-title"})

        url = self.urls['caranddr'][1] +  a['href']
        ttl = str(a.getText().strip())
        img = div.find('img')
        iul = img['src']
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site15(self, soup):
        '''ideas-ted'''
        sec = soup.find('section',attrs={"id":"block-container"})
        dvs = sec.find_all('div',attrs={"class":"post block animated fadeIn post"})
        div = dvs[randint(0,len(dvs)-1)]
        h2  = div.find('h2')
        a   = h2.find('a')

        url = a['href']
        ttl = str(a.getText().strip())
        img = div.find('img')
        iul = img['src']
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site16(self, soup):
        '''psychologytoday'''
        dvs = soup.find_all('div',attrs={"class":"blog-entry teaser-listing--item"})
        div = dvs[randint(0,len(dvs)-1)]

        img = div.find('img')
        iul = img['src']
        h2  = div.find('h2')
        a   = h2.find('a')
        url = self.urls['psycholg'][1] +  a['href']
        ttl = str(a.getText().strip())
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})


    def site17(self, soup):
        '''sunset'''
        ars = soup.find_all('article',attrs={"partial tile media image-top"})
        arc = ars[randint(0,len(ars)-1)]
        
        img = arc.find('img')
        iul = img['src']
        div = arc.find('div',attrs={"class":"headline"})
        a   = div.find('a')
        url = a['href']
        ttl = str(a.getText().strip())
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site18(self, soup):
        '''scientificamerican'''
        #第一条
        div = soup.find('div',attrs={"grid__col large-up-2-4 medium-2-2 small-hide"})
        arc = div.find('article')
        a   = arc.find('a')

        url = a['href']
        img = a.find('img')
        src = img['src']
        ttl = img['alt']
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

        #第二条
        div = soup.find('div',attrs={"grid most-popular__grid"})
        ars = div.find_all('article',attrs={"class":"listing-wide"})
        arc = ars[randint(0,len(ars)-1)]
        a   = arc.find('a')

        url = a['href']
        img = a.find('img')
        src = img['src']
        ttl = img['alt']
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site19(self, soup):
        '''mentalfloss'''
        div = soup.find('div',attrs={"hero-section-carousel"})
        dvs = div.find_all('div',attrs={"class":"hero-article"})
        div = dvs[randint(0,len(dvs)-1)]

        img = div.find('img')
        iul = img['src']
        div = div.find('div',attrs={"class":"hero-article-headline"})
        a   = div.find('a')
        url = self.urls['mentalfl'][1] +  a['href']
        ttl = str(a.getText().strip())
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site20(self, soup):
        '''epicurious'''
        sec = soup.find('section', attrs={"featured-items"})
        ars = sec.find_all('article')
        arc = ars[randint(0,len(ars)-1)]
        a   = arc.find('a')

        url = self.urls['epicurio'][1] +  a['href']
        img = arc.find('img')
        iul = img['src']
        ttl = img['alt']
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site21(self, soup):
        '''aeon'''
        imp = re.compile(r"url\('.*'\)")
        div = soup.find('div',attrs={"class":"article-list container"})
        fig = div.find('figure')
        stl = fig['style']

        img = imp.search(stl)
        iul = img.group(1)
        a   = div.find('a',attrs={"article-card__title"})
        url = self.urls['aeonweb'][1] +  a['href']
        ttl = str(a.getText().strip())
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site22(self, soup):
        '''playboy'''
        div = soup.find('div',attrs={"class":"section-recirc"})
        scs = div.find_all('section',attrs={"class":"jumbotron jumbotron-fixed"})
        sec = scs[randint(0,len(scs)-1)]
        a   = sec.find('a',attrs={"class":"link-img"})

        url = a['href']
        img = sec.find('img')
        iul = img['src']
        ttl = img['alt']
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site23(self, soup):
        '''vanity'''
        #第一条
        div = soup.find('div',attrs={"class":"component-top-stories-module component component"})
        a   = div.find('a')
        url = self.urls['vanityfa'][1] +  a['href']
        img = a.find('img')
        iul = img['src']
        h3  = div.find('h3')
        ttl = str(h3.getText().strip())
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

        #第二条
        div = soup.find('div',attrs={"class":"component-brand-streams"})
        uls = div.find_all('ul',attrs={"class":"component component-listing"})
        ul  = uls[randint(0,len(uls)-1)]
        lis = ul.find('lis')
        li  = lis[randint(0,len(lis)-1)]
        a   = li.find('a',attrs={"class":"featured-item-image"})
        url = self.urls['vanityfa'][1] +  a['href']
        img = a.find('img')
        iul = img['src']
        h3  = li.find('h3')
        ttl = str(h3.getText().strip())
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site24(self, soup):
        '''travelandleisure'''
        sec = soup.find('section', attrs={"class":"content-section content-section-left clearf"})
        ars = sec.find_all('article')
        arc = ars[randint(0,len(ars)-1)]
        a   = arc.find('a')

        url = self.urls['travelad'][1] +  a['href']
        img = a.find('img')
        iul = img['src']
        h3  = arc.find('h3')
        a   = h3.find('a')
        ttl = str(a.getText().strip())
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site25(self, soup):
        '''cio'''
        div = soup.find('div',attrs={"homepage-crawl"})
        dvs = div.find_all('div',attrs={"class":"crawl-item content-item content"})
        div = dvs[randint(0,len(dvs)-1)]
        a   = div.find('a')
        
        url = a['href']
        img = a.find('img')
        iul = img['src']
        h3  = div.find('h3')
        a   = h3.find('a')
        ttl = str(a.getText().strip())
        self.infos.append({ 'url':url, 'iul':iul, 'ttl':ttl+'<br>'})

    def site26(self, soup):
        '''computerworld'''
        div = soup.find('div',attrs={"homepage-crawl"})
        dvs = div.find_all("class":"crawl-item content-item content"})
        div = dvs[randint(0,len(dvs)-1)]

        img = div.find('img')
        iul = img['src']
        h3  = div.find('h3')
        a   = h3.find('a')
        url = self.urls['computew'][1] +  a['href']
        ttl = str(a.getText().strip())
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
 
    
    kind = 'it'
    url = 'https://www.computerworld.com'
    spider = SocietyNews()
    spider.getHtml(kind, url)
    #spider.downloadInfosT()
    #spider.downloadInfos()
    #spider.printinfo()

    #spider.writePreSuf(pref, name, 'w')
    #spider.writeInfo2html(name)
    #spider.writePreSuf(suff, name, 'a')

    #'https://www.brides.com'
    #'https://www.aarp.org/magazine'
    #'https://zidbits.com'               
    #'https://www.travelagents.com'
    #'https://www.cookinglight.com'
    #'https://aeon.co'                   
    #'https://www.nationalgeographic.com'
    #'https://www.southernliving.com'    
    #'https://www.maxim.com'             
    #'https://www.rollingstone.com'      
    #'https://www.playboy.com'           
    #'https://www.vanityfair.com'        
    #'https://www.travelandleisure.com'  
    #'https://www.foodandwine.com'
    #'https://www.bostonglobe.com'
    #'https://www.cio.com'
    #'https://www.computerworld.com'
    #'https://adage.com'
    #'https://www.unitedmags.com'
    #'https://www.outdoorlife.com'
    #'https://www.interiordesign.net'
    #'https://www.winespectator.com'
    #'https://www.thetimes.co.uk'
    #'https://www.consumerreports.org'
