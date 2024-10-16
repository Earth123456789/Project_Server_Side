from django import template

register = template.Library()

@register.simple_tag
def sumfunc(participants):
    return sum(participants)

def totalprice(regis, price):
    return regis * price
