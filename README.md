--------
# 描述 #
-------

Linux下获取豆瓣各门类下的高质量书籍信息并整理成书单(pdf格式)。

# 使用 #
	1.首先将Text2docx放到/usr/bin/下
		$ sudo chown root Text2docx
		$ sudo chgrp root Text2docx
		$ sudo mv Text2docx /usr/bin/
	2.建立存放书单pdf文件的目录,如'/home/username/file/booklist/'
		$ sudo  mkdir /home/username/file/booklist/
	3.修改Booklist/recommendbook.py的self.save_fold(第23行)为上述目录(注意最后的斜杠要加上) 
	4.执行
		$ python3 recommendbook.py
	5.查看
		直接到/home/username/file/booklis/下查看书单pdf文件

# 依赖 #
<li>请使用python3</li>
<li>请使用pip2安装docx</li>
	$ sudo pip2 install docx==0.2.4 (不是pip3)

# 书单示例 #
![ekqGXF.png](https://s2.ax1x.com/2019/07/23/ekqGXF.png)
