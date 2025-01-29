from django.urls import path
from . import views

app_name = 'pdf'

urlpatterns = [
    path('',views.AcceptView.as_view(),name='accept'),
    path('data/<int:pk>',views.resume,name='resume'),
    path('download/',views.all.as_view(),name='download'),

]
