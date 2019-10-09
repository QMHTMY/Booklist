------------
# 兼容系统 #
------------
	Unix-like OS

--------
# 描述 #
-------
Linux下获取豆瓣不同种类书籍信息并整理成书单(pdf格式)。许多人不知道不同类的书籍哪些好，这个程序获取的书籍普遍是高质量的书籍(一份书单最多400本书，一共有145份书单）。
<li>1.爬取书籍信息按类别存储在相应的txt文件中，如: 中国文学.txt 小说.txt </li>
<li>2.利用Text2docx转换txt为docx文件，如：中国文学.docx 小说.docx</li>
<li>3.利用Docx2pdf转换docx为pdf文件，如：中国文学.pdf 小说.pdf</li>
<li>4.删除.txt和.docx等缀余文件</li>

# 依赖 #
<li>请使用python3</li>
<li>请安装依赖包</li>
	$ sudo pip3 install -r requirement.txt

# 使用 #
	1.首先将Text2docx和Docx2pdf放到/usr/bin/下
	  $ sudo chown root Text2docx Docx2pdf
	  $ sudo chgrp root Text2docx Docx2pdf
	  $ sudo chmod 755  Text2docx Docx2pdf
	  $ sudo mv Text2docx /usr/bin/
	  $ sudo mv Docx2pdf  /usr/bin/
	2.建立存放书单pdf文件的目录,如'/home/username/file/booklist/'
	  $ sudo mkdir /home/username/file/booklist/
	3.修改Booklist/booklist.py的self.save_fold(第23行)为上述目录(注意最后的斜杠要加上) 
	4.将category.csv放入上述目录
	  $ mv Booklist/category.csv /home/username/file/booklist/
	5.执行
	  $ python3 booklist.py
	6.最后
	  直接到/home/username/file/booklis/下查看书单pdf文件

# 书单示例 #
![ekqGXF.png](https://s2.ax1x.com/2019/07/23/ekqGXF.png)
