--------
# 描述 #
-------
Linux下获取豆瓣各门类下的高质量书籍信息并整理成书单(pdf格式)，主要很多人不知道各行各类哪些书好，这个程序获取的书籍普遍是高质量的书籍(一份书单最多400本书，一共有146份书单）。
<li>1.爬取书籍信息按类别存储在相应的txt文件中，如: 中国文学.txt</li>
<li>2.利用Text2docx转换txt为docx文件，如：中国文学.docx</li>
<li>3.利用Docx2pdf转换docx为pdf文件，如：中国文学.pdf</li>
<li>4.删除txt和docx等缀余文件</li>

# 使用 #
	1.首先将Text2docx放到/usr/bin/下
	  $ sudo chown root Text2docx
	  $ sudo chgrp root Text2docx
	  $ sudo chmod 755  Text2docx
	  $ sudo mv Text2docx /usr/bin/
	2.建立存放书单pdf文件的目录,如'/home/username/file/booklist/'
	  $ sudo mkdir /home/username/file/booklist/
	3.修改Booklist/booklist.py的self.save_fold(第23行)为上述目录(注意最后的斜杠要加上) 
	4.执行
	  $ python3 booklist.py
	5.最后
	  直接到/home/username/file/booklis/下查看书单pdf文件

# 依赖 #
<li>请使用python3</li>
<li>请安装依赖包</li>
	$ sudo pip3 install -r requirement.txt

# 书单示例 #
![ekqGXF.png](https://s2.ax1x.com/2019/07/23/ekqGXF.png)
