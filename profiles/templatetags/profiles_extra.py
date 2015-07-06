#-*- coding: utf-8 -*-

from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def subtract(value, arg):
    return value - arg


@register.filter
def timeDifference(created, current=None):
    if current == None:
        current = timezone.localtime(timezone.now())

    created = timezone.localtime(created)

    if current.year == created.year:
        if current.month == created.month:
            if current.day == created.day:
                if current.hour == created.hour:
                    if current.minute == created.minute:
                        return u"Az Önce"
                    else:
                        return str(current.minute - created.minute) + u"  dk. önce"
                else:
                    return str(current.hour - created.hour) + u"  saat önce"
            elif current.day - 1 == created.day:
                return u"Dün  " + str(created.hour) + ":" + str(created.minute)
            
        return str(created.day) + " " + str(created.mount) + " , " + str(created.hour) + ":" + str(created.minute)
    else:
        return created
        

