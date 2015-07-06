from django.contrib import admin

# Register your models here.

from .models import *
from .forms import *

class MaterialListInline(admin.TabularInline):
    model = MaterialList

class NewFood(admin.ModelAdmin):
    inlines = [MaterialListInline]
    list_display = ('name', 'addingDate')

admin.site.register(Food, NewFood)
admin.site.register(FoodKind)