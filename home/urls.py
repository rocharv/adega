from . import views
from django.urls import path, include


app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    path('help/about/', views.help_about, name='help_about'),
    path('help/entities/', views.help_entities, name='help_entities'),
    path('help/examples/', views.help_examples, name='help_examples'),
    path('login/', views.hlogin, name='hlogin'),
    path('logout/', views.hlogout, name='hlogout'),
    path(
        'change_password/',
        views.change_password,
        name='change_password'
    ),
]
