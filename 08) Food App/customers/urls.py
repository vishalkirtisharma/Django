from django.urls import path
from vendor import views as AccountsViews
from . import views

urlpatterns = [
    path('', AccountsViews.custdashboard, name='customer'),
    path('profile/', views.cprofile, name='cprofile'),
]
