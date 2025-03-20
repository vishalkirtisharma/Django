from django.urls import path,include
from . import models,views
from vendor.views import registervendor,login,logout,dashboard,myaccounts,custdashboard,vendordashboard

urlpatterns = [
    path('registeruser/',views.registeruser,name='registeruser'),
    path('registervendor/',registervendor,name='registervendor'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('myaccounts/',myaccounts,name='myaccounts'),
    path('dashboard/',dashboard,name='dashboard'),
    path('custdashboard/',custdashboard,name='custdashboard'),
    path('vendordashboard/',vendordashboard,name='vendordashboard'),
    path('activate/<uidb64>/<token>/', views.activate,name='activate'),
    path('forgot_password/', views.forgot_password,name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>', views.reset_password_validate,name='reset_password_validate'),
    path('reset_password/', views.reset_password,name='reset_password'),
    path('', myaccounts),
    path('vendor/', include('vendor.urls')),
]
