import xadmin

from relation.models import Client, Media


class ClientAdmin(object):
    """ xadmin客户管理 """
    list_display = ('name', 'call', 'qq', 'phone', 'types', 'remark')
    list_filter = ['types']
    search_fields = ['name', 'call', 'qq', 'phone']
    model_icon = 'fa fa-jpy'
    list_export = ''  # 禁止导出数据
    show_bookmarks = False  # 关闭书签功能


xadmin.site.register(Client, ClientAdmin)


class MediaAdmin(object):
    """ xadmin媒体管理 """
    list_display = ('name', 'call', 'qq', 'phone', 'remark')
    # list_filter = ['name']
    search_fields = ['name', 'call', 'qq', 'phone']
    model_icon = 'fa fa-random'
    list_export = ''  # 禁止导出数据
    show_bookmarks = False  # 关闭书签功能


xadmin.site.register(Media, MediaAdmin)
