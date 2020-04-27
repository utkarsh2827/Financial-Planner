from django import template

register = template.Library()

@register.filter(name = 'profit')
def profit(c):
    print(c.curr_price)
    return (c.curr_price-float(c.initial_price))*float(c.quantity_owned)