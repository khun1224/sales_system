����Ŀʹ��Python����Django�����������


ʹ�ñ���������linuxϵͳCentOS7.x���粻ʹ�ñ����������аٶȣ�
1����װ�����Ժ��Ȱ�װ LAMP ���� LANP�Ķ��С�
2������̵�-->Ӧ������-->python-->��װPython��Ŀ������-->��װ�ú�ѡ��汾����װpython3.7.x
3������̵�-->Python��Ŀ������-->�����Ŀ---> python3.7 ---> ���ѡ�� django---> ������ʽѡ��uwsgi---> �˿��Զ��壨һ��Ϊ8000�������Զ��壬�����ڱ�����ȫ�����￪�Ŵ˶˿ڣ�---> ·��ѡ�����ｫweb�ϴ���������(���磺/www/wwwroot/sales_system/) ---> �����ļ�/�ļ���ѡ����Ŀ��·���µ�sales_system(���磺/www/wwwroot/sales_system/sales_system) ---> �Ƿ�װģ�������Ϳ����������빴ѡ��
4��ӳ����վ��������
5����python��Ŀ����������������������������Ȼ�޷����ʾ�̬��Դ���ϴ���ͼƬ(static�Ǿ�̬��ԴĿ¼��media���û��ϴ���ͼƬĿ¼)�������ʾ�˿�����ʹ������ֹͣ����������
	static-map=/static=/www/wwwroot/sales_system/static/
	static-map=/media=/www/wwwroot/sales_system/media/
6�����ݿ�������ڱ���Ŀ��·���µ�sales_system/setting.py������
7�����뵽�����Ŀ¼����/www/wwwroot/sales_system/ ��ʹ������������⻷�� ������������ source ��Ŀ·��/��Ŀ��_venv/bin/activate
8���� ��Ŀ·����ִ��������� python manage.py collectstatic ���ռ���̬�ļ�����python manage.py makemigrations ��Ǩ�����ݿ⣩��python manage.py migrate ���������ݿ⣩��python manage.py createsuperuser ��������������Ա����
9������nginx��uwsgi ���ɷ��� 


https://blog.csdn.net/bocai_xiaodaidai/article/details/94395604  django-xadmin��ʹ��(�ȹٷ��ĵ�������)

