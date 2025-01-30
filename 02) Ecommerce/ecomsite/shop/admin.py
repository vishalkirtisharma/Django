from django.contrib import admin
from . import models
# Register your models here.

admin.site.site_header = 'E-Commerce site'
admin.site.site_title = 'E-Commerce site'
admin.site.index_title= 'abc shopping'


class ProductAdmin(admin.ModelAdmin):

    def change_category_to_default(self,request,queryset):
        queryset.update(category='default')
    change_category_to_default.short_description = 'Change category'
    list_display = ('title','price','discount_price','category','description','image')
    search_fields = ['title','category']
    actions = ('change_category_to_default',)
    list_editable = ('price','discount_price','image')

admin.site.register(models.ProductsModel,ProductAdmin)
admin.site.register(models.OrderModel)