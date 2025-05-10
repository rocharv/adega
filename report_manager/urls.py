from . import views
from django.urls import path

app_name = "report_manager"
urlpatterns = [
    path('list_by_category/', views.list_by_category, name='list_by_category'),
    # path('list_by_items/', views.list_by_items, name='list_by_items'),
    path('list_all_api/', views.list_all_api, name='list_all_api'),
]
