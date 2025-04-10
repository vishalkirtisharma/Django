from django.contrib import admin
from . import models

# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'fooditem','quantity','updated_at')

admin.site.register(models.Cart,CartAdmin)