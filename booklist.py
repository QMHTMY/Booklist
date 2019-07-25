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
#    下载豆瓣图书分类标签并生成各分类书籍阅读书单
#
#    Copyright 2019 
#    All Rights Reserved!

import re,time,csv
import random
import requests
import datetime
from os import chdir,getcwd
from bs4 import BeautifulSoup as Soup
from os.path import basename, exists
from subprocess import call
from multiprocessing import Pool

class DoubanBookList():
    '''豆瓣图书分类生产器'''
    def __init__(self,author='Shieber'):
        self.rooturl1 = 'https://book.douban.com/tag'               #分类图书主页
        self.rooturl2 = 'https://book.douban.com'                   #构造分页url的根url
        self.download = 10                                          #下载进程数 
        self.maxpage  = 20                                          #获取该类书最大页数
        self.heading  = '豆瓣读书推荐书单'                          #pdf书单抬头信息 
        self.author   = author                                      #pdf书单作者姓名
        self.datetime = self.getDateTime()                          #pdf书单创建日期
        self.storedir = '/home/shieber/Files/gitp/Douban/booklist/' #书单存储位置
        self.order    = {                                           #系统调用的指令
                          'txt2docx':'Text2docx -a 1>/dev/null 2>&1',
                          'docx2pdf':'libreoffice --convert-to pdf *.docx 1>/dev/null 2>&1',
                          'txt2pdf' :'Text2pdf -a 1>/dev/null 2>&1'
                        }
                         
        self.headers  = {
                          'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; \
                           rv:68.0) Gecko/20100101 Firefox/68.0',
                          'Connection':'close'
                        } 
        self.ip_list  = ['144.217.229.155', '49.51.195.24', '192.99.191.239', \
                         '49.51.68.122', '49.51.70.42', '101.4.136.34', \
                         '124.192.27.246', '192.95.3.198', '203.195.168.154']
        self.http_ips = ['https://'+ip for ip in self.ip_list]

    def getDateTime(self):
        '''获取当前日期'''
        time = datetime.datetime.now()
        if time.month < 10:
            mnth = ''.join(['0',str(time.month)])  
        else:
            mnth = str(time.month)

        if time.day < 10:
            day  = ''.join(['0',str(time.day)])  
        else:
            day  = str(time.day)

        date = ''.join([' ',str(time.year),'.',mnth,'.',day])
        return date

    def getSpecificInfo(self,info):
        '''去除文字中的空格和换行符'''
        if info:
            info = str(info.getText())
            info = info.replace(' ','').replace('\n','')
        else:
            info = '暂无'
        return info

    def getInfo(self,soup):
        if not soup:
            return []

        Info = []
        booklist = soup.find_all('li',class_="subject-item")
        for book in booklist:
            book  = book.find('div',class_='info')
            title = self.getSpecificInfo(book.find('a'))
            authr = self.getSpecificInfo(book.find('div',class_='pub'))
            score = self.getSpecificInfo(book.find('span',class_='rating_nums'))
            descs = self.getSpecificInfo(book.find('p'))

            info  ={
                    'title':title,
                    'authr':authr,
                    'score':score,
                    'descs':descs
                   }
            Info.append(info)

        return Info 

    def getBookInfo(self,pageurls,proxy):
        '''返回所有书籍的详细信息列表'''
        if not pageurls:
            return []

        bookinfo = []
        for url in pageurls:
            soup = self.getFromUrl(url,proxy)
            info = self.getInfo(soup)
            bookinfo += info
            time.sleep(0.2)                      #强制等待，避免频繁抓取
        return bookinfo 

    def getInfoPlusPageUrls(self,url):
        soup = self.getFromUrl(url,proxy=False)
        if not soup:
            return [],[]

        bookinfo = self.getInfo(soup)

        pageurls = []
        pagenums = soup.find_all('a',href=re.compile(r'/tag/.*?start=\d+&type=T'))
        if pagenums:
            maxpage = int(pagenums[-2].getText())
            for page in range(1,min(self.maxpage,maxpage)):
                item = '?start=%d&type=T'%(page*20)
                newurl  = ''.join([url,item])
                pageurls.append(newurl)

        return bookinfo, pageurls

    def deleteTxtDocx(self,delete=False):
        '''删除中间产生的txt,docx文件'''
        if delete:
            cwd = getcwd()
            chdir(self.storedir)
            call('rm *.txt  >/dev/null 2>&1',shell=True) 
            call('rm *.docx >/dev/null 2>&1',shell=True) 
            chdir(cwd)

    def fileTransfer(self,success,key):
        if not success:
            return False

        cwd = getcwd()
        chdir(self.storedir)
        call(self.order[key],shell=True)
        chdir(cwd)

    def save2Txt(self,url,bookinfos):
        '''依据bookinfo生成该类别书籍书单的pdf文件'''
        if not bookinfos:
            return False

        txtname = ''.join([self.storedir,basename(url),'.txt'])
        with open(txtname,'w') as txtObj:
            txtObj.write(''.join([' '*42,self.heading,'(',basename(url),')','\n'])) #标题
            txtObj.write(''.join([' '*29,self.author,self.datetime,'\n']))          #时间
            for i, infodic in enumerate(bookinfos):
                txtObj.write(''.join([str(i+1),'\n']))                              #书籍序号
                txtObj.write(''.join(['　　书名：', infodic['title'], '\n']))
                txtObj.write(''.join(['　　作者：', infodic['authr'], '\n']))
                txtObj.write(''.join(['　　评分：', infodic['score'], '\n']))
                txtObj.write(''.join(['　　简介：', infodic['descs'], '\n']))
                txtObj.write('\n')                                                  #书间空行

    def saveBookList(self,url,proxy):
        '''获取书籍信息并保存'''
        bookinfo1, pageurls = self.getInfoPlusPageUrls(url)
        bookinfo2 = self.getBookInfo(pageurls,proxy)
        bookinfos = bookinfo1 + bookinfo2
        self.save2Txt(url,bookinfos)

    def multiSave(self,urls,s=1,e=145,multi=False,proxy=False):
        '''多进程循环获取所有书籍信息并保存'''
        if urls:
            if e < len(urls):
                urls = urls[s-1:e]

            if multi:
                pool = Pool(self.download)
                for url in urls:
                    pool.apply_async(self.saveBookList,(url,proxy))
                pool.close()
                pool.join()
                return True
            else:
                for url in urls:
                    self.saveBookList(url,proxy)
                return True
        else:
            return False

    def save2csv(self,urls):
        csvname  = self.storedir + 'category.csv'
        if not exists(csvname):
            with open(csvname,'w',newline='') as csvObj:
                csv_writer = csv.writer(csvObj,dialect='excel')
                for i,url in enumerate(urls):
                    csv_writer.writerow([i,url])

    def readFromcsv(self,csvname):
        bookurls = []
        with open(csvname,encoding='utf-8') as csvObj:
            csv_reader = csv.reader(csvObj)
            for row in csv_reader:
                bookurls.append(row[1]) 
        return bookurls

    def getBookCateUrls(self):
        '''
           获取所有分类的主页url
           若本地存储有就读取本地的
        '''
        bookurls = []
        csvname  = self.storedir + 'category.csv'
        if exists(csvname):
            return self.readFromcsv(csvname)

        soup = self.getFromUrl(self.rooturl1,proxy=False)
        if not soup:
            return []

        bookcates = soup.find_all('a',href=re.compile(r'/tag/.*'))
        for cate in bookcates:
            bookurl = ''.join([self.rooturl2, cate['href']])
            bookurls.append(bookurl) 
        
        self.save2csv(bookurls[1:])               
        return bookurls[1:]                  #第1个url不需要

    def getFromUrl(self,url,proxy=False):
        '''prox控制是否开启代理'''
        requests.session().keep_alive = False
        if proxy:
            prox = {'https':random.choice(self.http_ips)}
            resp = requests.get(url,headers=self.headers,proxies=prox)
        else:
            resp = requests.get(url,headers=self.headers)


        if 200 == resp.status_code:
            resp.encoding = 'utf-8'
            soup = Soup(resp.content,'html.parser')
            if soup:
                return soup
            else:
                return []
        else:
            return []

if __name__ == "__main__":
    #s起始书单序列号，e截止书单序列号 (s最小1,e最大145)，multi:多线程，proxy:ip代理

    # Step I 下载书籍信息到txt文件
    start = time.time()
    booklist = DoubanBookList()              
    cateurls = booklist.getBookCateUrls() 
    success  = booklist.multiSave(cateurls,s=1,e=len(cateurls),multi=True,proxy=False) 
    end = time.time()
    print('下载耗时：%.2f(m)'%(end-start)/60)

    # Step II 转换txt为pdf并删除中间文件
    start = time.time()
    booklist.fileTransfer(success,key='txt2docx')
    booklist.fileTransfer(success,key='docx2pdf')
    booklist.deleteTxtDocx(delete=True)
    end = time.time()
    print('转换耗时：%.2f(m)'%(end-start)/60)
