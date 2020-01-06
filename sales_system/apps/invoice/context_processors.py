import datetime
import calendar
from datetime import timedelta

from django.db.models import Q, Sum

from invoice.models import OrderRefund


def get_current_user(request):
    """ 根据用户ID获得数据 """
    # get_id = request.session.get('_auth_user_id')
    user = request.user
    admin = request.user.is_superuser

    # 查看当前日期
    now = datetime.date.today()  # 今天
    yesterday = now - timedelta(days=1)  # 昨天

    # 获取本周第一天和最后一天
    this_week_start = now - timedelta(days=now.weekday())
    this_week_end = now + timedelta(days=6 - now.weekday())

    # 上周第一天和最后一天
    last_week_start = now - timedelta(days=now.weekday() + 7)
    last_week_end = now - timedelta(days=now.weekday() + 1)

    # 本月第一天和最后一天
    this_month_start = datetime.date(now.year, now.month, 1)
    this_month_end = datetime.date(now.year, now.month, now.day)

    # 上月第一天和最后一天
    last_month_end = this_month_start - timedelta(days=1)
    last_month_start = datetime.date(last_month_end.year, last_month_end.month, 1)

    if user.is_authenticated and admin is False:
        # 今日订单总量,开单,退款
        today_total_orders = OrderRefund.objects.filter(
            Q(user_id=user) & Q(created_at=now)).count()
        today_success_orders = OrderRefund.objects.filter(
            Q(user_id=user) & Q(created_at=now) & Q(types=10)).count()
        today_refund_orders = OrderRefund.objects.filter(
            Q(user_id=user) & Q(created_at=now) & Q(types=20)).count()

        # 查询今日，昨日，本周的毛利
        profit_today = OrderRefund.objects.filter(
            Q(user_id=user) & Q(created_at=now)).aggregate(profit=Sum('profit'))['profit']
        profit_yesterday = OrderRefund.objects.filter(
            Q(user_id=user) & Q(created_at=yesterday)).aggregate(profit=Sum('profit'))['profit']
        profit_this_week = OrderRefund.objects.filter(
            Q(user_id=user) & Q(created_at__range=(this_week_start, this_week_end))).aggregate(
            profit=Sum('profit'))['profit']

        # 查询本月，上月，本月相差的毛利
        profit_this_month = OrderRefund.objects.filter(
            Q(user_id=user) & Q(created_at__range=(this_month_start, this_month_end))).aggregate(
            profit=Sum('profit'))['profit']
        profit_last_month = OrderRefund.objects.filter(
            Q(user_id=user) & Q(created_at__range=(last_month_start, last_month_end))).aggregate(
            profit=Sum('profit'))['profit']
        if profit_last_month is not None and profit_this_month is not None:
            profit_month_gap = profit_last_month - profit_this_month  # 毛利差
        else:
            profit_month_gap = 0

        # 本月总量，上月总量，本月总量相差
        this_month_total_orders = OrderRefund.objects.filter(
            Q(user_id=user) & Q(created_at__range=(this_month_start, this_month_end))).count()
        last_month_total_orders = OrderRefund.objects.filter(
            Q(user_id=user) & Q(created_at__range=(last_month_start, last_month_end))).count()
        if last_month_total_orders is not None and this_month_total_orders is not None:
            month_total_orders_gap = last_month_total_orders - this_month_total_orders  # 总量差
        else:
            month_total_orders_gap = 0

        # 本月成交总量，上月成交，成交相差
        this_month_success_orders = OrderRefund.objects.filter(
            Q(user_id=user) & Q(types=10) & Q(created_at__range=(this_month_start, this_month_end))).count()
        last_month_success_orders = OrderRefund.objects.filter(
            Q(user_id=user) & Q(types=10) & Q(created_at__range=(last_month_start, last_month_end))).count()
        if last_month_success_orders is not None and this_month_success_orders is not None:
            month_success_orders_gap = last_month_success_orders - this_month_success_orders  # 成交差
        else:
            month_success_orders_gap = 0

        # 本月退款总量，上月退款，退款相差
        this_month_refund_orders = OrderRefund.objects.filter(
            Q(user_id=user) & Q(types=20) & Q(created_at__range=(this_month_start, this_month_end))).count()
        last_month_refund_orders = OrderRefund.objects.filter(
            Q(user_id=user) & Q(types=20) & Q(created_at__range=(last_month_start, last_month_end))).count()
        if last_month_refund_orders is not None and this_month_refund_orders is not None:
            month_refund_orders_gap = last_month_refund_orders - this_month_refund_orders  # 成交差
        else:
            month_refund_orders_gap = 0

    else:
        # 今日订单总量,开单,退款
        today_total_orders = OrderRefund.objects.filter(Q(is_valid=True) & Q(created_at=now)).count()
        today_success_orders = OrderRefund.objects.filter(Q(is_valid=True) & Q(created_at=now) & Q(types=10)).count()
        today_refund_orders = OrderRefund.objects.filter(Q(is_valid=True) & Q(created_at=now) & Q(types=20)).count()

        # 查询今日，昨日，本周的毛利
        profit_today = OrderRefund.objects.filter(
            Q(is_valid=True) & Q(created_at=now)).aggregate(profit=Sum('profit'))['profit']
        profit_yesterday = OrderRefund.objects.filter(
            Q(is_valid=True) & Q(created_at=yesterday)).aggregate(profit=Sum('profit'))['profit']
        profit_this_week = OrderRefund.objects.filter(
            Q(is_valid=True) & Q(created_at__range=(this_week_start, this_week_end))).aggregate(profit=Sum('profit'))['profit']

        # 查询本月，上月，本月相差的毛利
        profit_this_month = OrderRefund.objects.filter(
            Q(is_valid=True) & Q(created_at__range=(this_month_start, this_month_end))).aggregate(profit=Sum('profit'))['profit']
        profit_last_month = OrderRefund.objects.filter(
            Q(is_valid=True) & Q(created_at__range=(last_month_start, last_month_end))).aggregate(profit=Sum('profit'))['profit']
        if profit_last_month is not None and profit_this_month is not None:
            profit_month_gap = profit_last_month - profit_this_month  # 毛利差
        else:
            profit_month_gap = 0

        # 本月总量，上月总量，总量相差
        this_month_total_orders = OrderRefund.objects.filter(
            Q(is_valid=True) & Q(created_at__range=(this_month_start, this_month_end))).count()
        last_month_total_orders = OrderRefund.objects.filter(
            Q(is_valid=True) & Q(created_at__range=(last_month_start, last_month_end))).count()
        if last_month_total_orders is not None and this_month_total_orders is not None:
            month_total_orders_gap = last_month_total_orders - this_month_total_orders  # 总量差
        else:
            month_total_orders_gap = 0

        # 本月成交总量，上月成交，成交相差
        this_month_success_orders = OrderRefund.objects.filter(
            Q(is_valid=True) & Q(types=10) & Q(created_at__range=(this_month_start, this_month_end))).count()
        last_month_success_orders = OrderRefund.objects.filter(
            Q(is_valid=True) & Q(types=10) & Q(created_at__range=(last_month_start, last_month_end))).count()
        if last_month_success_orders is not None and this_month_success_orders is not None:
            month_success_orders_gap = last_month_success_orders - this_month_success_orders  # 成交差
        else:
            month_success_orders_gap = 0

        # 本月退款总量，上月退款，退款相差
        this_month_refund_orders = OrderRefund.objects.filter(
            Q(is_valid=True) & Q(types=20) & Q(created_at__range=(this_month_start, this_month_end))).count()
        last_month_refund_orders = OrderRefund.objects.filter(
            Q(is_valid=True) & Q(types=20) & Q(created_at__range=(last_month_start, last_month_end))).count()
        if last_month_refund_orders is not None and this_month_refund_orders is not None:
            month_refund_orders_gap = last_month_refund_orders - this_month_refund_orders  # 成交差
        else:
            month_refund_orders_gap = 0

    return {
        'user': user,
        'admin': admin,

        # 今日订单总量,开单,退款
        'today_total_orders': today_total_orders,
        'today_success_orders': today_success_orders,
        'today_refund_orders': today_refund_orders,

        # 查询今日，昨日，本周的毛利
        'profit_today': profit_today,
        'profit_yesterday': profit_yesterday,
        'profit_this_week': profit_this_week,

        # 查询本月，上月，本月相差的毛利
        'profit_this_month': profit_this_month,
        'profit_last_month': profit_last_month,
        'profit_month_gap': profit_month_gap,

        # 本月总量，上月总量，本月总量相差
        'this_month_total_orders': this_month_total_orders,
        'last_month_total_orders': last_month_total_orders,
        'month_total_orders_gap': month_total_orders_gap,

        # 本月成交总量，上月成交，成交相差
        'this_month_success_orders': this_month_success_orders,
        'last_month_success_orders': last_month_success_orders,
        'month_success_orders_gap': month_success_orders_gap,

        # 本月退款总量，上月退款，退款相差
        'this_month_refund_orders': this_month_refund_orders,
        'last_month_refund_orders': last_month_refund_orders,
        'month_refund_orders_gap': month_refund_orders_gap,
    }
