from . import views
from django.urls import path, include


app_name = views.APP_STR
urlpatterns = [
    path('create/<str:ttype>/', views.create_new, name='create_new'),
    path('delete/', views.delete_bulk, name='delete_bulk'),
    path('edit/<int:id>/', views.edit_id, name='edit_id'),
    path('list/', views.list_all, name='list_all'),
    path('list_all_api/', views.list_all_api, name='list_all_api'),
    path('view/<int:id>/', views.view_id, name='view_id'),
]
