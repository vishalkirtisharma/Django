from django.contrib import admin
from . import models
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)} 
    list_display = ('category_name','vendor')
    search_fields = ('category_name','vendor__vendor_name')

class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('food_title',)} 
    list_display = ('food_title','category','price','vendor','is_available','updated_at')
    search_fields = ('food_title','vendor__vendor_name','category__category_name','price')
    list_filter =('is_available',)



admin.site.register(models.Category,CategoryAdmin)
admin.site.register(models.FoodItem,FoodItemAdmin)