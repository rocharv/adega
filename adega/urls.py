"""
URL configuration for adega project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('', include("home.urls")),
    path('admin/', admin.site.urls),
    path(
        'address_manager/',
        include('address_manager.urls'),
        name='address_manager'
    ),
    path(
        'company_manager/',
        include('company_manager.urls'),
        name='company_manager'
    ),
    path(
        'person_manager/',
        include('person_manager.urls'),
        name='person_manager'
    ),
    path(
        'category_manager/',
        include('category_manager.urls'),
        name='category_manager'
    ),
    path(
        'warehouse_manager/',
        include('warehouse_manager.urls'),
        name='warehouse_manager'
    ),
    path(
        'item_manager/',
        include('item_manager.urls'),
        name='item_manager'
    ),

    path("select2/", include("django_select2.urls")),
]
