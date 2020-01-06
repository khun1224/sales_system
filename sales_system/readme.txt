本项目使用Python语言Django框架来制作。


使用宝塔来部署，linux系统CentOS7.x（如不使用宝塔，请自行百度）
1、安装宝塔以后，先安装 LAMP 或者 LANP的都行。
2、软件商店-->应用搜索-->python-->安装Python项目管理器-->安装好后选择版本管理安装python3.7.x
3、软件商店-->Python项目管理器-->添加项目---> python3.7 ---> 框架选择 django---> 启动方式选择uwsgi---> 端口自定义（一般为8000，可以自定义，必须在宝塔安全设置里开放此端口）---> 路径选择这里将web上传到服务器(例如：/www/wwwroot/sales_system/) ---> 启动文件/文件夹选择本项目跟路径下的sales_system(例如：/www/wwwroot/sales_system/sales_system) ---> 是否安装模块依赖和开机启动必须勾选。
4、映射网站（域名）
5、在python项目管理器里必须配置以下两条命令，不然无法访问静态资源和上传的图片(static是静态资源目录，media是用户上传的图片目录)，如果提示端口正在使用请先停止运行在配置
	static-map=/static=/www/wwwroot/sales_system/static/
	static-map=/media=/www/wwwroot/sales_system/media/
6、数据库的配置在本项目跟路径下的sales_system/setting.py下配置
7、进入到程序跟目录例如/www/wwwroot/sales_system/ ，使用命令进入虚拟环境 在命令行输入 source 项目路径/项目名_venv/bin/activate
8、在 项目路径上执行以下命令： python manage.py collectstatic （收集静态文件），python manage.py makemigrations （迁移数据库），python manage.py migrate （创建数据库），python manage.py createsuperuser （创建超级管理员）。
9、重启nginx和uwsgi 即可访问 


https://blog.csdn.net/bocai_xiaodaidai/article/details/94395604  django-xadmin的使用(比官方文档更精简)

