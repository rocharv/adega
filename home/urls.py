from . import views
from django.urls import path, include


app_name = 'home'
urlpatterns = [
    path('', views.home_index, name='home_index'),
    path('help/', views.home_help, name='home_help'),
    path('login/', views.home_login, name='home_login'),
    path('logout/', views.home_logout, name='home_logout'),
]
