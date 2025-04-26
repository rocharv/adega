from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_index, name='home_index'),
    path('login/', views.home_login, name='home_login'),
    path('logout/', views.home_logout, name='home_logout'),
]
