from . import views
from django.urls import path, include


app_name = views.APP_STR
urlpatterns = [
    path('list/', views.list_all, name='list_all'),
    path('list_all_api/', views.list_all_api, name='list_all_api'),
]
