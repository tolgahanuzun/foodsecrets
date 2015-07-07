#-*- coding: utf-8 -*-

from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator

class MaterialKind(models.Model):
    kind = models.CharField(primary_key=True, max_length=10, verbose_name=u"Adı")

    class Meta:
        verbose_name = u"Malzeme Türü"
        verbose_name_plural = u"Malzeme Türleri"

        ordering = ["kind"] 

    def __unicode__(self):
        return self.kind


class Material(models.Model):
    name = models.CharField(primary_key=True, db_index=True, max_length=100, verbose_name=u"Adı")
    material_kind = models.ForeignKey(MaterialKind, verbose_name=u"Tür")
    amount = models.IntegerField(validators=[MinValueValidator(1),
                                      MaxValueValidator(2000)], verbose_name="Miktar")
    calorie = models.FloatField(validators=[MinValueValidator(1),
                                      MaxValueValidator(2000)], verbose_name="Kalori")


    class Meta:
        verbose_name = u"Malzeme"
        verbose_name_plural = u"Malzemeler"

        ordering = ["name"] 

    def __unicode__(self):
        return self.name + " ( " + str(self.amount) + " " + self.material_kind.kind + " = " + str(self.calorie) + " kalori ) "
