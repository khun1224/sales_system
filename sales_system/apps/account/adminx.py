import xadmin
from xadmin import views


class BaseSetting(object):
    """xadmin的基本配置"""
    enable_themes = True  # 开启主题切换功能
    use_bootswath = True  # 这一行也得添加上才行


class GlobalSettings(object):
    """xadmin的全局配置"""
    site_title = "开单管理系统"  # 设置站点标题
    site_footer = "兴荣网络"  # 设置站点的页脚
    # menu_style = "accordion"  # 设置菜单折叠


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
