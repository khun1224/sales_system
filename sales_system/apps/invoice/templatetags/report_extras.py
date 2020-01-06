import locale
from decimal import Decimal

from django import template

register = template.Library()


def accounting(value, place=2):
    """ 用逗号分隔数据 """
    try:
        place = int(place)
    except:
        place = 2

    try:
        value = Decimal(value)
        locale.setlocale(locale.LC_ALL, '')
        return locale.format("%.*f", (place, value), 1)
    except Exception as e:
        return value


def minus(value1, value2):
    """ 减法 """
    try:
        value = value1 - value2
    except Exception as e:
        value = None
    return value


register.filter('accounting_format', accounting)
register.filter('minus', minus)
