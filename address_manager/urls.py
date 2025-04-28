from django.urls import path, include
from . import views

urlpatterns = [
    path('create/', views.address_create, name='address_create'),
    path('delete/', views.address_delete, name='address_delete'),
    path('edit/', views.address_edit, name='address_edit'),
    path('list/', views.address_list, name='address_list'),
    path('view/<int:id>/', views.address_view, name='address_view'),

    path('addresses/', views.address_list_api, name='address_list_api')
]
