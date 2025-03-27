from django.urls import path
from . import views
from accounts import views as accountsviews
urlpatterns = [
    path('registervendorsss', views.registervendor, name='registervendors'),
    path('profile/', views.vprofile, name='vprofile'),
    path('',views.vendordashboard ,name='vendor'),
    path('menu_builder/', views.menu_builder, name='menu_builder'),
    path('menu_builder/category/<int:pk>/', views.fooditems_by_category, name='fooditems_by_category'),

    # Curd Category
    path('menu_builder/category/add/', views.add_category, name='add_category'),
    path('menu_builder/category/edit/<int:pk>', views.edit_category, name='edit_category'),
    path('menu_builder/category/delete/<int:pk>', views.delete_category, name='delete_category'),
    
    # Food Item Curd
    path('menu_builder/food_add/', views.add_food, name='add_food'),
    path('menu_builder/food_edit/<int:pk>', views.edit_food, name='edit_food'),
    path('menu_builder/food_edit/delete/<int:pk>', views.delete_food, name='delete_food'),

]
