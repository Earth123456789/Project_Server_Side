from django import template

register = template.Library()

@register.simple_tag
def sumfunc(participants):
    return sum(participants)
