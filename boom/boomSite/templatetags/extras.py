from django import template

register = template.Library()

@register.filter(name='winner')
def subtract(value):
    return value[0][0]
@register.filter(name='second')
def subtract(value2):
    return value2[1][0]
@register.filter(name='third')
def subtract(value3):
    return value3[2][0]

@register.filter(name='time')
def time(value):
    return value[0][1]
@register.filter(name='time2')
def time(value):
    return value[1][1]
@register.filter(name='time3')
def time(value):
    return value[2][1]