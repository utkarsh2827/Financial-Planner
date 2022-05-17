from django import template

register = template.Library()

@register.filter(name = 'cprofit')
def cprofit(c):
    print(c['curr_price'])
    return c['curr_price']*float(c['quantity_owned'])