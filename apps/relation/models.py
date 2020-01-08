from django.db import models

from utils import constants


class CommonUtils(models.Model):
    """ 公共工具 使用抽象的方法，这段是不会生成sql表"""

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        abstract = True


class Client(CommonUtils):
    """ 客户 """
    name = models.CharField('客户名称', max_length=32, unique=True)
    call = models.CharField('微信', max_length=32, null=True, blank=True)
    qq = models.CharField('QQ', max_length=32, null=True, blank=True)
    phone = models.CharField('手机', max_length=32, null=True, blank=True)
    types = models.SmallIntegerField('客户类别', null=False, blank=False,
                                     choices=constants.CLIENT_TYPE_CHOICES)
    remark = models.TextField('备注', max_length=256, null=True, blank=True)

    class Meta:
        db_table = 'relation_client'
        verbose_name = '客户'
        verbose_name_plural = '客户'

    def __str__(self):
        return self.name


class Media(CommonUtils):
    """ 媒体 """
    name = models.CharField('媒体名称', max_length=64, unique=True)
    call = models.CharField('微信', max_length=32, null=True, blank=True)
    qq = models.CharField('QQ', max_length=32, null=True, blank=True)
    phone = models.CharField('手机', max_length=32, null=True, blank=True)
    remark = models.TextField('备注', max_length=256, null=True, blank=True)

    class Meta:
        db_table = 'relation_media'
        verbose_name = '媒体'
        verbose_name_plural = '媒体'

    def __str__(self):
        return self.name
