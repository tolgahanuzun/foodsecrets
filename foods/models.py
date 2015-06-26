#-*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from profiles.models import * 
from materials.models import *


class Food(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name=u"Adı")
    description = models.TextField(max_length=1000, verbose_name=u"Tarif")
    user = models.ForeignKey(User, verbose_name=u"Kullanıcı")

    class Meta:
        verbose_name = u"Yemek"
        verbose_name_plural = u"Yemekler"

        ordering = ["name"] 

    def __unicode__(self):
        return self.name


class MaterialList(models.Model):
    name = models.ForeignKey(Material, verbose_name=u"ADI")
    amount = models.IntegerField(validators=[MinValueValidator(1),
                                      MaxValueValidator(2000)], verbose_name=u"Miktar")
    food = models.ForeignKey(Food, verbose_name=u"Yemek")


    class Meta:
        verbose_name = u"Malzeme Listesi"
        verbose_name_plural = u"Malzeme Listeleri"

        ordering = ["name"] 

    def __string__(self):
        return self.name
 