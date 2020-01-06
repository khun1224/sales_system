from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum

import xadmin

from invoice.models import OrderRefund, Report
from utils.tools import set_invalid, set_valid


class OrderAdmin(object):
    """ 开单/退款 """
    list_display = ('types', 'sales', 'created_at', 'is_valid', 'recharge', 'client', 'media', 'media_rebate',
                    'bank_name', 'bank_account', 'bank', 'client_rebate', 'receipt',
                    'pay', 'profit', 'remark')
    list_filter = ('types', 'sales', 'is_valid', 'media', 'client', 'created_at')
    # search_fields = ('sn', 'sales', 'client__name', 'media__name', 'created_at')
    list_per_page = 10  # 分页的页数
    readonly_fields = ('sn', 'profit')  # 不可编辑，在界面上可见
    exclude = ('is_valid',)  # 排除，在页面上无法显示
    model_icon = 'fa fa-gavel'
    list_export = ''  # 禁止导出数据
    show_bookmarks = False  # 关闭书签功能
    reversion_enable = True
    # 可以使用聚合函数
    aggregate_fields = {'receipt': 'sum', 'pay': 'sum', 'profit': 'sum'}

    def queryset(self):
        """函数作用：使当前登录的用户只能看到自己负责的设备"""
        qs = super(OrderAdmin, self).queryset()
        if self.request.user.is_superuser:
            return qs
        # return qs.filter(area_company=User.objects.get(user=self.request.user))
        return qs.filter(user_id=self.request.user)

    def instance_forms(self):
        """ 添加订单时，自动添加当前用户的id """
        super(OrderAdmin, self).instance_forms()
        # 判断是否为新建操作，新建操作才会设置user_id的默认值
        if not self.org_obj:
            self.form_obj.initial['user_id'] = self.request.user.id


class ReportAdmin(object):
    """ 报表 """

    # 指向自定义的页面
    object_list_template = 'report.html'
    list_display = ('types', 'is_valid', 'date_format', 'sales_color', 'client', 'media', 'recharge_color',
                    'media_rebate_color', 'client_rebate_color', 'receipt_color', 'pay_color', 'profit_color', 'remark')
    list_filter = ('types', 'sales', 'is_valid', 'media', 'client', 'created_at')
    model_icon = 'fa fa-bar-chart-o'
    readonly_fields = ('sn', 'user_id')  # 不可编辑，在界面上可见
    exclude = ('is_valid',)  # 排除，在页面上无法显示
    list_per_page = 10  # 分页的页数
    actions = [set_invalid, set_valid]  # 批量审核/反审核
    show_bookmarks = False  # 关闭书签功能

    def get_context(self):
        """ 重写方法，把要展示的数据更新到context """
        context = super().get_context()

        # 从数据库查出的结果集
        invoice_all = OrderRefund.objects.all()

        # 查询结果集，使总数能随着筛选进行改变
        filter_conditions = {}
        for k, v in self.request.GET.items():
            if '_p_' in k:
                key = k.split('_p_')
                filter_conditions[key[1]] = v

        # 打款总和
        sum_pay = OrderRefund.objects.filter(is_valid=True)\
            .filter(**filter_conditions)\
            .aggregate(pay=Sum('pay'))
        # 收款总和
        sum_receipt = OrderRefund.objects.filter(is_valid=True)\
            .filter(**filter_conditions)\
            .aggregate(receipt=Sum('receipt'))
        #############################################################
        # 分页器   这是自定义的report.html的分页器
        page_size = 5  # 一页显示多少条数据
        paginator = Paginator(invoice_all, page_size)
        page = self.request.GET.get('page')

        try:
            page_data = paginator.page(page)
        except PageNotAnInteger:
            page_data = paginator.page(1)
        except EmptyPage:
            page_data = paginator.page(paginator.num_pages)

        # page_data = paginator.get_page(page)
        ##############################################################
        try:
            # 总利润 = 收款总和 - 收款总和
            all_profit = sum_receipt['receipt'] - sum_pay['pay']
        except TypeError:
            all_profit = 0

        context.update(
            {
                'invoice_all': invoice_all,  # 自定义的页面才需要用到
                'sum_pay': sum_pay,
                'sum_receipt': sum_receipt,
                'all_profit': all_profit,
                'page_data': page_data,  # 自定义的页面才需要用到
            }
        )

        return context


xadmin.site.register(OrderRefund, OrderAdmin)
xadmin.site.register(Report, ReportAdmin)
