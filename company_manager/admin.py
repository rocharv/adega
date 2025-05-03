from django.contrib import admin
from.models import Company


admin.site.register(Company)
autocomplete_fields = ['address']