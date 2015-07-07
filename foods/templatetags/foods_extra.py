#-*- coding: utf-8 -*-

from django import template

register = template.Library()

@register.filter(is_safe=True)
def totalCalories(material):
    value = material.amount / float(material.material.amount)
    value *= material.material.calorie

    return value