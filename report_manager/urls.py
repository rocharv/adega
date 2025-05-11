from . import views
from django.urls import path

app_name = "report_manager"
urlpatterns = [
    path('list_by/<str:list_type>/', views.list_by, name='list_by'),
    path('list_by/api/<str:list_type>/', views.list_by_api, name='list_by_api'),
]
