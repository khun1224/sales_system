"""sales_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import xadmin
# version模块自动注册需要版本控制的 Model
from xadmin.plugins import xversion
xadmin.autodiscover()
xversion.register_models()


urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'', xadmin.site.urls, name='xadmin'),
    path(r'account/', include('account.urls', namespace='account')),


    # 报表模块 方式一
    # path('report/', include(('report.urls', 'report'), namespace='report'))
    # 方式二，需要在每个app目录下的urls添加app_name = 'xxx'
    # path('report/', include('report.urls', namespace='report'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

