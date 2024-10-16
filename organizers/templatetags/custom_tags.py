from django import template

register = template.Library()

@register.simple_tag
def sumfunc(participants):
    return sum(participants)

@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={'class': css_class})
