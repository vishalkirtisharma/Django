from django.contrib import admin
from . import models
# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    list_display = ['user','vendor_name','is_approved','created_at']
    list_display_links  =('user','vendor_name',)
    list_editable = ('is_approved',)


class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = ('vendor','day','from_hour','to_hour')

admin.site.register(models.Vendor,VendorAdmin) 
admin.site.register(models.OpeningHours) 