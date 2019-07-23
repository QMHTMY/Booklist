#!/usr/bin/python3
# coding:utf-8
#
# Author: Shieber
# Date: 2019.07.23
#
# 下载豆瓣图书分类标签并生成各分类书籍阅读书单
# 

import os,re,time
import requests
import subprocess
import datetime
from bs4 import BeautifulSoup as Soup
from os.path import basename 
from multiprocessing import Pool

class DoubanBookList():
    '''豆瓣图书分类生产器'''
    def __init__(self,author='Shieber'):
        self.root_url1 = 'https://book.douban.com'
        self.root_url2 = 'https://book.douban.com/tag'
        self.save_fold = '/home/shieber/Files/gitp/Douban/booklist/'
        self.headers   = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; \
                           rv:68.0) Gecko/20100101 Firefox/68.0'} 
        self.datetime  = self.getDateTime() #日期
        self.author    = author             #pdf创建者姓名
        self.max       = 20                 #获取最大页数

    def getDateTime(self):
        '''获取当前日期'''
        time = datetime.datetime.now()
        year = str(time.year)
        mnth = str(time.month)
        day  = str(time.day)

        if time.month < 10:
            mnth = ''.join(['0',mnth])  
        if time.day < 10:
            day = ''.join(['0',day])  

        date = ''.join([' ',year,'.',mnth,'.',day,'\n'])
        return date

    def getMaxPage(self,book_url):
        '''获取该分类下图书最后一页的页码以构造所有页的url'''
        page_resp = requests.get(book_url,headers=self.headers)
        if 200 != page_resp.status_code:
            return None

        page_resp.encoding = 'utf-8'
        soup = Soup(page_resp.content,'html.parser')
        if not soup:
            return None 

        patn = re.compile(r'/tag/.*?start=\d+&type=T')
        page_nums = soup.find_all('a',href=patn)
        if page_nums:
            maxpage = int(page_nums[-2].getText())
            return maxpage
        else:
            return None

    def makePageUrl(self,book_url,maxpage):
        '''生成该分类下每一页的url，不超过20页'''
        page_urls = []

        if not maxpage: #若只有一页
            page_urls.append(book_url)
        else:
            for page in range(min(self.max,maxpage)):
                item = '?start=%d&type=T'%(page*20)
                url  = ''.join([book_url,item])
                page_urls.append(url)

        return page_urls

    def getBookInfo(self,page_urls):
        '''返回所有书籍的详细信息列表'''
        bookinfo = []
        for page_url in page_urls:
            page_resp = requests.get(page_url,headers=self.headers)
            if 200 != page_resp.status_code:
                return None
            page_resp.encoding = 'utf-8'

            soup = Soup(page_resp.content,'html.parser')
            if not soup:
                return None

            book_list = soup.find_all('li',class_="subject-item")
            for book in book_list:
                book  = book.find('div',class_='info')

                info  = book.find('a')
                title = str(info['title'])
                info  = book.find('div',class_='pub')
                author= str(info.getText())
                author= author.replace(' ','').replace('\n','') #去除空格和换行符
                info  = book.find('span',class_='rating_nums')
                score = str(info.getText())
                info  = book.find('p')
                desc  = str(info.getText())
                desc  = desc.replace('\n','')                   #去除换行符

                info  = {
                            'title':title,
                            'author':author,
                            'score':score,
                            'desc':desc
                        }

                bookinfo.append(info)

        return bookinfo 
    
    def makeBookTxt(self,url_base,txtname,bookinfo):
        '''依据bookinfo生成该类别书籍书单的pdf文件'''
        if not bookinfo:
            return None

        with open(txtname,'w') as txtObj:
            txtObj.write(''.join([' '*42,'豆瓣读书推荐书单(',url_base,')\n'])) #标题
            txtObj.write(''.join([' '*29,self.author,self.datetime]))          #时间
            for i, dic in enumerate(bookinfo):
                txtObj.write(''.join([str(i+1),'\n']))                         #书籍序号
                txtObj.write(''.join(['　　书名：',dic['title'] ,'\n']))
                txtObj.write(''.join(['　　作者：',dic['author'],'\n']))
                txtObj.write(''.join(['　　评分：',dic['score'] ,'\n']))
                txtObj.write(''.join(['　　简介：',dic['desc']  ,'\n\n']))

    def makeBookDocx(self):
        '''将目录下所有txt转换为docx'''
        cwd = os.getcwd()
        os.chdir(self.save_fold)
        subprocess.call('Text2docx -a',shell=True)
        os.chdir(cwd)
        time.sleep(1)

    def makeBookPdf(self):
        '''将目录下所有docx转换为pdf'''
        cwd = os.getcwd()
        os.chdir(self.save_fold)
        subprocess.call('libreoffice --invisible --convert-to pdf *.docx',shell=True)
        os.chdir(cwd)

    def getBookUrls(self,prt=False):
        '''获取所有分类的主页url'''
        root_resp= requests.get(self.root_url2,headers=self.headers)
        if 200 != root_resp.status_code:
            return None
        root_resp.encoding = 'utf-8'
        soup = Soup(root_resp.content,'html.parser')

        if not soup:
            return None
        patn = re.compile(r'/tag/.*')
        book_cates = soup.find_all('a',href=patn)

        book_urls  = []
        for book_cate in book_cates:
            book_url = ''.join([ self.root_url1, book_cate['href'] ])
            book_urls.append(book_url) 

        if prt:              #控制打印出url
            for url in book_urls[1:]:
                print(url)

        return book_urls[1:] #第0个url不是需要的

    def getBookText(self,book_url):
        '''获取书籍信息并保存'''
        url_base  = basename(book_url)
        txtname   = ''.join([self.save_fold,url_base,'.txt'])
        maxpage   = self.getMaxPage(book_url)
        page_urls = self.makePageUrl(book_url,maxpage)
        bookinfo  = self.getBookInfo(page_urls)
        self.makeBookTxt(url_base,txtname,bookinfo)

    def multiGet(self,book_urls):
        '''多进程循环获取所有书籍信息并保存'''
        if not book_urls:
            return None

        pool = Pool(10)
        for book_url in book_urls:
            pool.apply_async(self.getBookText,(book_url,))
        pool.close()
        pool.join()

if __name__ == "__main__":
    booklist  = DoubanBookList(author='Shieber') #可修改，比如author='Trump' 
    book_urls = booklist.getBookUrls()           #2019.07.23有145个图书类别
    booklist.multiGet(book_urls)
    booklist.makeBookDocx()
    booklist.makeBookPdf()
