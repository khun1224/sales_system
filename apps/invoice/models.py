from django.contrib.auth.models import User
from django.db import models
from django.utils.html import format_html

from relation.models import Client, Media
from utils.constants import INVOICE_TYPES_CHOICES
from utils.tools import gen_trans_id


class OrderRefund(models.Model):
    """ 开单/退款 """
    # 记录创建该数据的用户
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='创建者', null=True, related_name='user_id',
                                help_text='<span style="color:red">默认是自己的用户名，注意检查，不然无法查看自己的订单</span>')
    sn = models.CharField('开单编号', max_length=64, default=gen_trans_id)
    types = models.SmallIntegerField('开单/退款', choices=INVOICE_TYPES_CHOICES, null=False, blank=False)
    sales = models.CharField('销售', max_length=32)
    img = models.ImageField('图片附件', upload_to='%Y%m', null=True, blank=True)
    recharge = models.FloatField('账户币', max_length=64)
    client = models.ForeignKey(Client, verbose_name='客户', on_delete=models.CASCADE, related_name='client', null=True,
                               blank=True)
    media = models.ForeignKey(Media, verbose_name='媒体', on_delete=models.CASCADE, related_name='media', null=True,
                              blank=True)
    media_rebate = models.FloatField('媒体返点', max_length=32)
    bank_name = models.CharField('账户名称', max_length=64)
    bank_account = models.CharField('银行账号', max_length=64)
    bank = models.CharField('开户行', max_length=64)
    client_rebate = models.FloatField('给客户返点', max_length=10)
    receipt = models.DecimalField('收款', max_digits=10, decimal_places=2,
                                  help_text='<span style="color:red">退款时在前面加个减号,除于客户返点,收款的数值一定要大于打款</span>')
    pay = models.DecimalField('打款', max_digits=10, decimal_places=2,
                              help_text='<span style="color:red">退款时在前面加个减号,除于媒体返点,收款的数值一定要大于打款</span>')
    profit = models.DecimalField('毛利', max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateField('创建时间', auto_now_add=True)
    updated_at = models.DateField('修改时间', auto_now=True)
    remark = models.TextField('备注', max_length=256, null=True, blank=True)
    is_valid = models.BooleanField('审核', default=False)

    class Meta:
        db_table = 'invoice'
        verbose_name = '开单/退款'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return '流水号：' + self.sn

    def save(self, *args, **kwargs):
        self.profit = self.receipt - self.pay
        super().save(*args, **kwargs)
        return self.profit


class Report(OrderRefund):
    """ 报表 """

    def date_format(self):
        """ 日期格式化 """
        if self.types == 10:
            color_code = 'black'
            result = self.created_at.strftime('%Y-%m-%d')
        else:
            color_code = 'red'
            result = self.created_at.strftime('%Y-%m-%d')
        return format_html(
            '<span style="color:{0};">{1}</span>',
            color_code,
            result,
        )

    def sales_color(self):
        """ 销售的颜色设定 """
        if self.types == 10:
            color_code = 'black'
            result = self.sales
        else:
            color_code = 'red'
            result = self.sales
        return format_html(
            '<span style="color:{0};">{1}</span>',
            color_code,
            result,
        )

    def recharge_color(self):
        """ 账户币的颜色设定 """
        if self.types == 10:
            color_code = 'black'
            result = self.recharge
        else:
            color_code = 'red'
            result = self.recharge
        return format_html(
            '<span style="color:{0};">{1}</span>',
            color_code,
            result,
        )

    def media_rebate_color(self):
        """ 媒体返点的颜色设定 """
        if self.types == 10:
            color_code = 'black'
            result = self.media_rebate
        else:
            color_code = 'red'
            result = self.media_rebate
        return format_html(
            '<span style="color:{0};">{1}</span>',
            color_code,
            result,
        )

    def client_rebate_color(self):
        """ 客户返点的颜色设定 """
        if self.types == 10:
            color_code = 'black'
            result = self.client_rebate
        else:
            color_code = 'red'
            result = self.client_rebate
        return format_html(
            '<span style="color:{0};">{1}</span>',
            color_code,
            result,
        )

    def receipt_color(self):
        """ 收款的颜色设定 """
        if self.types == 10:
            color_code = 'black'
            result = self.receipt
        else:
            color_code = 'red'
            result = self.receipt
        return format_html(
            '<span style="color:{0};">{1}</span>',
            color_code,
            result,
        )

    def pay_color(self):
        """ 打款的颜色设定 """
        if self.types == 10:
            color_code = 'black'
            result = self.pay
        else:
            color_code = 'red'
            result = self.pay
        return format_html(
            '<span style="color:{0};">{1}</span>',
            color_code,
            result,
        )

    def profit_color(self):
        """ 自定义毛利字段颜色 """
        if self.types == 10:
            color_code = 'black'
            result = self.profit
        else:
            color_code = 'red'
            result = self.profit
        return format_html(
            '<span style="color:{0};">{1}</span>',
            color_code,
            result,
        )

    profit_color.short_description = '毛利'
    profit_color.admin_order_field = 'created_at'  # 指定排序依据

    date_format.short_description = '创建日期'
    sales_color.short_description = '销售'
    recharge_color.short_description = '账户币'
    media_rebate_color.short_description = '媒体返点'
    client_rebate_color.short_description = '客户返点'
    receipt_color.short_description = '收款'
    pay_color.short_description = '打款'

    date_format.admin_order_field = 'created_at'  # 指定排序依据
    recharge_color.admin_order_field = 'recharge'  # 指定排序依据
    receipt_color.admin_order_field = 'receipt'  # 指定排序依据
    pay_color.admin_order_field = 'pay'  # 指定排序依据

    class Meta:
        verbose_name = '报表与审核'
        verbose_name_plural = verbose_name
        proxy = True
