## 使用说明

1. 将项目`clone`下来（任意位置都可）

   `git clone http://gitlab-devops.pook.com/airtest_qa/xxmjj_script.git`

2. 使用[VsCode](https://bokecloud.pook.com.cn/f/db55741ee18e4106903b/?dl=1)或者[PyCharm](https://bokecloud.pook.com.cn/f/19864a59f84f4eb18ec9/?dl=1)打开刚才`clone`下来的项目（这两个软件的安装包，云存储上均有，可直接下载安装）

3. 第一层的文件夹为自己名字拼音缩写，请自己在提交代码的时候创建好，后续自己的代码都提交至这个文件夹下

4. 请在自己电脑上安装`Git`工具，[下载地址](https://bokecloud.pook.com.cn/f/7c21b9979cd34860898b/?dl=1)

5. 提交时可以使用`VsCode`、`PyCharm`提交，也可使用命令提交，命令提交方式如下）（cd到项目目录下）

   > 如不是很熟悉命令行的这些操作，建议还是利用VsCode或PyCharm来进行拉取、提交等操作

```
1. git pull origin master    	# 这里是为了在提交之前保持本地代码是最新的代码
2. git add .                 	# 这里的“.”意思就是当前目录下所有文件，也可替换成自己的的文件夹名字
3. git commit -m "***********" # 这里是给提交加提交说明
4. git push -u origin master   # 这里是推送提交 
```



