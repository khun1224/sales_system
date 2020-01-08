import random
from datetime import datetime

from django.contrib import messages


def gen_trans_id():
    """ 生成交易流水 """
    now = datetime.now()
    str_date = now.strftime('%Y%m%d%H%M%S%f')
    return str_date + str(random.randint(1000, 9999))


def set_invalid(modeladmin, request, queryset):
    """ 批量禁用 is_valid=False """
    queryset.update(is_valid=False)
    messages.success(request, '反审核-操作成功')


def set_valid(modeladmin, request, queryset):
    """ 批量启用 is_valid=True """
    # if request.user.id_superuser:
    queryset.update(is_valid=True)
    messages.success(request, '审核-操作成功')


set_invalid.short_description = '反审核'
set_valid.short_description = '审核'


