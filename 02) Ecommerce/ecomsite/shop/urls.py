from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('<int:id>',views.detail,name='product'),
    path('checkout',views.checkout,name='checkout'),
]
