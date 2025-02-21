from django.urls import path
from .  import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:id>', views.detail_view, name='details'),
    path('success/',views.payment_sucesss_view,name='success'),
    path('failed/',views.payment_failed_view,name='failed'),
    path('register',views.register,name='register'),
    path('createproduct',views.create_product,name='createproduct'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('editproduct/<int:id>',views.product_edit,name='editproduct'),
    path('delete/<int:id>',views.product_delete,name='delete'),
    path('api/checkout-session/<int:id>',views.create_checkout_session,name='api_checkout_session'),
    path('login/', auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='myapp/logout.html'), name='logout'),
    path('invalid/', views.invalid, name='invalid'),
    path('purchases/', views.my_purchase, name='purchases'),
    path('sales/', views.sales, name='sales'),
    ]
