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

    month_information = {"1":u"Ocak", "2":u"Şubat", "3":u"Mart", "4":"Nisan", 
                         "5":u"Mayıs", "6":u"Haziran", "7":u"Temmuz", "8":u"Ağustos", 
                         "9":"Eylül", "10":u"Ekim","11":u"Kasım", "12":u"Aralık"} 

    print created
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
                if str(created.minute) == "0":
                    return u"Dün  ," + str(created.hour) + ":" + str(created.minute) + "0"
                elif len(str(created.minute)) == 1:
                    return u"Dün  ," + str(created.hour) + ":" + "0" + str(created.minute)
                else:
                    return u"Dün  ," + str(created.hour) + ":" + str(created.minute)

        month = month_information[str(created.month)]
        if str(created.minute) == "0":    
            return str(created.day) + " " + month + " , " + str(created.hour) + ":" + str(created.minute) + "0"
        elif len(str(created.minute)) == 1:
            return str(created.day) + " " + month + " , " + str(created.hour) + ":" + "0" + str(created.minute)
        else:
            return str(created.day) + " " + month + " , " + str(created.hour) + ":" + str(created.minute)
    else:
        month = month_information[str(created.month)]
        if str(created.minute) == "0":    
            return str(created.day) + " " + month + " " +str(created.year) +" , " + str(created.hour) + ":" + str(created.minute) + "0"
        elif len(str(created.minute)) == 1:
            return str(created.day) + " " + month + " " +str(created.year) +" , " + str(created.hour) + ":" + "0" + str(created.minute)
        else:
            return str(created.day) + " " + month + " " +str(created.year) +" , " + str(created.hour) + ":" + str(created.minute) 
        

