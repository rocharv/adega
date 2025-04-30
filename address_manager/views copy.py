from .forms import CrudForm
from django.apps import apps
from django.contrib import messages
from django.db import transaction
from django.db.models import (
    ForeignKey, ManyToManyField, Model, OneToOneField, Q
)
from django.http import JsonResponse
<<<<<<< HEAD
from django.shortcuts import render, redirect
=======
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import AddressForm
from .models import Address
>>>>>>> 8f9aac7 (feat: better definition of domains in urls.)


# Dynamic import of a class model described by MODEL_STR
APP_STR = "address_manager"
MODEL_STR = "Address"
try:
    MODEL: Model = apps.get_model(APP_STR, MODEL_STR)
except ImportError:
    MODEL: Model = None
    raise ImportError(
        f"Model {MODEL_STR} not found in app {APP_STR}. "
        f"Please check the model name and app name."
    )

# Constants to define crud operations
ENTITY_PLURAL = "addresses"
ALL_FIELDS = [
    field.name.split('.')[-1] for field in MODEL._meta.get_fields()
        if not field.primary_key and not
        isinstance(field, (ForeignKey, OneToOneField, ManyToManyField))
]
TABLE_COLUMNS = { # Insert here the columns you want to show in the table
    0: 'id', # this is mandatory
    1: 'street',
    2: 'number',
    3: 'city',
    4: 'state',
    5: 'created_at',
}
VERBOSE_NAME = MODEL._meta.verbose_name.lower()
VERBOSE_NAME_PLURAL = MODEL._meta.verbose_name_plural.lower()

def get_match_in_any_column_query(search_value):
    query = Q()
    for field in ALL_FIELDS:
        query = query | Q(**{f"{field}__icontains": search_value})
    return query

def address_create(request):
    ACTION = "Incluir " + VERBOSE_NAME
    if request.method == "POST":
        form = CrudForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                VERBOSE_NAME + " anterior criada(o) com sucesso."
            )
            # clear the form
            form = CrudForm()
        else:
            messages.error(
                request,
                VERBOSE_NAME + " anterior não foi criado(a)."
            )
            # return the form with errors
    else:
        form = CrudForm()
    return render(
<<<<<<< HEAD
        request, APP_STR + "/create_view.html",
=======
        request, "address_manager/create_edit_view.html",
>>>>>>> 8f9aac7 (feat: better definition of domains in urls.)
        {'form': form, 'action': ACTION},
    )

def address_delete(request):
    ACTION = "Excluir " + VERBOSE_NAME
    # Get the entity object by id
    if request.method == "POST":
        # delete all related ids in a single atomic bulk transaction
        ids = request.POST.getlist('selected_rows[]')
        with transaction.atomic():
            MODEL.objects.filter(id__in=ids).delete()

    return redirect(reverse("address_manager:address_list"))

def address_edit(request, id):
    ACTION = "Editar " + VERBOSE_NAME
    # Get the address object by id
    entity = MODEL.objects.get(id=id)
    # Create the form with the address object
    if request.method == "POST":
        form = CrudForm(request.POST, instance=entity)
        if form.is_valid():
            form.save()
    else:
        form = CrudForm(instance=entity)
    return render(
<<<<<<< HEAD
        request, APP_STR + "/create_view.html",
=======
        request, "address_manager/create_edit_view.html",
>>>>>>> 8f9aac7 (feat: better definition of domains in urls.)
        {'form': form, 'action': ACTION},
    )

def address_list(request):
    ACTION = "Listar/Editar/Apagar " + VERBOSE_NAME_PLURAL
    entities = MODEL.objects.all()
    return render(
        request, APP_STR + "/list.html",
        {
            ENTITY_PLURAL: entities,
            'action': ACTION},
    )

def address_list_api(request):
    # Get DataTables parameters
    draw = int(request.GET.get('draw', 0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')
    order_column_index = int(request.GET.get('order[0][column]', 0))
    order_dir = request.GET.get('order[0][dir]', 'asc')

    # Get the field name from mapping,
    # default to 'id' if index is out of bounds
    order_column_name = TABLE_COLUMNS.get(order_column_index, 'id')
    if order_dir == 'desc':
        order_column_name = f"-{order_column_name}"

    # Base QuerySet
    queryset = MODEL.objects.all()

    # Total records count before filtering
    records_total = queryset.count()

    # Filter records based on search value, matching any column
    if search_value:
        queryset = queryset.filter(
            get_match_in_any_column_query(search_value)
        )
    records_filtered = queryset.count()

    # Apply sorting and pagination
    queryset = (
        queryset.order_by(order_column_name).distinct()[start:start + length]
    )

    # Prepare data field for JSON response to DataTables
    data = []
    row = []
    for qs in queryset:
        row.clear()
        for col in TABLE_COLUMNS.values():
            col_value = getattr(qs, col)
            row.append(col_value)
        data.append(row.copy())

    # Format JSON Response to DataTables request
    response = {
        'draw': draw,
        'recordsTotal': records_total,
        'recordsFiltered': records_filtered,
        'data': data,
    }
    return JsonResponse(response)

def address_view(request, id):
    ACTION = "Visualizar detalhes de " + VERBOSE_NAME
    # Get the entity object by id
    entity = MODEL.objects.get(id=id)
    # Create the form with the entity object
    form = CrudForm(instance=entity, is_view_only=True)
    return render(
<<<<<<< HEAD
        request, APP_STR +"/create_view.html",
=======
        request, "address_manager/create_edit_view.html",
>>>>>>> 8f9aac7 (feat: better definition of domains in urls.)
        {'form': form, 'action': ACTION},
    )
