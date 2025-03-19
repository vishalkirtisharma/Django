from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CustomUserAdmin(UserAdmin):
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    list_display = ('email','first_name','last_name','username','role','is_active')
    ordering = ('-date_joined',)


admin.site.register(models.User,CustomUserAdmin)
admin.site.register(models.UserProfile)

