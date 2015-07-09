#-*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

from profiles.models import * 
from materials.models import *

class MealKind(models.Model):
    kind = models.CharField(primary_key=True, max_length=100, verbose_name=u"Adı")

    class Meta:
        verbose_name = u"Yemek Türü"
        verbose_name_plural = u"Yemek Türleri"

        ordering = ["kind"] 

    def __unicode__(self):
        return self.kind

class Meal(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name=u"Adı")
    description = models.TextField(max_length=1000, verbose_name=u"Tarif")
    user = models.ForeignKey(User, verbose_name=u"Kullanıcı")
    meal_kind = models.ForeignKey(MealKind, verbose_name=u"Tür")
    totalCalories = models.FloatField(default=0, blank=True, verbose_name=u"Toplam Kalori")
    addingDate = models.DateTimeField(auto_now_add=True, verbose_name=u"Eklenme Tarihi")
    favourite = models.IntegerField(default=0, blank=True, verbose_name=u"Popülerliği")
    image = models.ImageField(default=None, blank=True, upload_to="meal", verbose_name="Yemek Resmi")

    class Meta:
        verbose_name = u"Yemek"
        verbose_name_plural = u"Yemekler"

        ordering = ["name"] 

    def __unicode__(self):
        return self.name

class MaterialList(models.Model):
    material = models.ForeignKey(Material, verbose_name=u"ADI")
    amount = models.IntegerField(validators=[MinValueValidator(1),
                                      MaxValueValidator(2000)], verbose_name=u"Miktar")
    meal = models.ForeignKey(Meal, verbose_name=u"Yemek")


    class Meta:
        verbose_name = u"Malzeme Listesi"
        verbose_name_plural = u"Malzeme Listeleri"

        ordering = ["meal"] 

    def __string__(self):
        return self.material
 