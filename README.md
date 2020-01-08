# sales_system
广告推广销售统计

广告推广公司销售开单用的，记录媒体和客户的信息和每天消耗的账户币。

sales_system/setting.py   ---本项目的配置文件
数据库以及生产环境下需要开启debug=False都在setting.py下配置
开启debug=False时需要执行python manage.py collectstatic 收集静态文件到static

本项目跟路径上执行以下命令： 
python manage.py makemigrations （迁移数据库）
python manage.py migrate （创建数据库）
python manage.py createsuperuser （创建超级管理员）

python manage.py runserver （本地启动本项目）

浏览器输入http://127.0.0.1:8000/
