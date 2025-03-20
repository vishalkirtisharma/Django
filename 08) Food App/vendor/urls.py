from django.urls import path
from . import views
from accounts import views as accountsviews
urlpatterns = [
    path('registervendorsss', views.registervendor, name='registervendors'),
    path('profile/', views.vprofile, name='vprofile'),
    path('',views.vendordashboard ,name='vendor'),

]
