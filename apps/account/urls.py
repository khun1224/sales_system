from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from account import views

app_name = 'account'

urlpatterns = [
    path('user_register/', views.user_register, name='user_register'),
    path('success/', views.success, name='success'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
