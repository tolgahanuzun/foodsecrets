#-*- coding: utf-8 -*-

from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def subtract(value, arg):
    return value - arg


@register.filter
def hasMeal(mealList, meal):
    if meal in mealList:
        return True
    else:
        return False

@register.filter
def timeDifference(created, current=None):
    if current == None:
        current = timezone.localtime(timezone.now())

    created = timezone.localtime(created)

    print timezone.now()

    if current.year == created.year:
        if current.month == created.month:
            if current.day == created.day:
                if current.hour == created.hour:
                    if current.minute == created.minute:
                        return u"Az Önce"
                    else:
                        return str(current.minute - created.minute) + u"  dk. önce"
                elif current.hour-1 == created.hour:
                    different_minute = current.minute + ( 60 - created.minute )

                    if different_minute < 60:
                        return str(different_minute) + u"  dk önce."
                    elif different_minute >= 119:
                        return "2 saat önce"
                    elif different_minute >= 60:
                        return "1 saat önce"

                else:
                    return str(current.hour - created.hour) + u"  saat önce"
            elif current.day - 1 == created.day:
                return u"Dün  ," + str(created.hour) + ":" + str(created.minute)
            
        return str(created.day) + " " + str(created.mount) + " , " + str(created.hour) + ":" + str(created.minute)
    else:
        return created
        

