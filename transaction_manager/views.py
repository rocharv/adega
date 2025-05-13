from .forms import CrudForm
from django.apps import apps
from django.contrib import messages
from django.db import transaction
from django.db.models import ForeignKey, Model, Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

## Make changes here -------------------------------------------------------
APP_STR = "transaction_manager"
MODEL_STR = "Transaction"
TABLE_COLUMNS = {
    0: 'id', # this is mandatory (don't remove)
    1: 'warehouse',
    2: 'type',
    3: 'invoice',
    4: 'quantity',
    5: 'item',
}
KEPT_FIELDS_AFTER_SUCCESSFUL_CREATE = [
    'warehouse',
    'type',
    'invoice',
    'actor',
    'company_counterpart',
    'person_counterpart',
    'beginning_date',
]
## -------------------------------------------------------------------------

# Dynamic import of a class model described by MODEL_STR
try:
    MODEL: Model = apps.get_model(APP_STR, MODEL_STR)
except ImportError:
    MODEL: Model = None
    raise ImportError(
        f"Model {MODEL_STR} not found in app {APP_STR}. "
        f"Please check the model name and app name."
    )

FK_FIELDS = [
    field.name for field in MODEL._meta.get_fields()
    if isinstance(field, ForeignKey) and field.name != "id"
]

VERBOSE_NAME = MODEL._meta.verbose_name
VERBOSE_NAME_PLURAL = MODEL._meta.verbose_name_plural

VERBOSE_COLUMN_LIST = []
for field in TABLE_COLUMNS.values():
    VERBOSE_COLUMN_LIST.append(
        MODEL._meta.get_field(field).verbose_name
    )
def get_match_in_any_column_query(search_value):
    """
    Creates a query object that matches the search_value in any of the fields
    defined in TABLE_COLUMNS, including foreign key fields. For foreign key
    fields, it searches on their string representation.
    """
    query = Q()
    for field in TABLE_COLUMNS.values():
        # Special case for FK fields
        if field == "warehouse":
            query |= Q(**{f"{field}__name__icontains": search_value})
            query |= Q(**{f"{field}__company__name__icontains": search_value})
        elif field == "item":
            query |= Q(**{f"{field}__category__name__icontains": search_value})
            query |= Q(**{f"{field}__corporate_tag__icontains": search_value})
            query |= Q(**{f"{field}__serial_number__icontains": search_value})
        elif field == "company_counterpart":
            query |= Q(**{f"{field}__name__icontains": search_value})
        elif field == "person_counterpart":
            query |= Q(**{f"{field}__full_name__icontains": search_value})
        elif field == "actor":
            query |= Q(**{f"{field}__full_name__icontains": search_value})
        else:
            # Search on regular fields
            query |= Q(**{f"{field}__icontains": search_value})
    return query

def create_new(request, ttype: str):
    ACTION = "Incluir " + VERBOSE_NAME
    TRANSACTION_TYPE = ttype

    # Create the form with the address object
    if request.method == "POST":
        form = CrudForm(
            request.POST,
            crud_form_type="create",
            transaction_type=TRANSACTION_TYPE,
        )
        if form.is_valid():
            form.save()
            messages.success(
                request,
                VERBOSE_NAME + " anterior criado(a) com sucesso."
            )
            # Create a new form but copies fields
            # in KEPT_FIELDS_AFTER_SUCCESSFUL_CREATE
            kept_data ={}
            for field in KEPT_FIELDS_AFTER_SUCCESSFUL_CREATE:
                kept_data[field] = form.cleaned_data[field]
            form = CrudForm(
                crud_form_type="create",
                initial=kept_data,
                transaction_type=TRANSACTION_TYPE,
            )
            return render(
                request,
                APP_STR + "/create_edit_view.html",
                {'form': form, 'action': ACTION},
            )
    else:
        # request method is GET
        form = CrudForm(
            crud_form_type="create",
            transaction_type=TRANSACTION_TYPE,
        )
    return render(
        request,
        APP_STR + "/create_edit_view.html",
        {'form': form, 'action': ACTION},
    )

def delete_bulk(request):
    if request.method == "POST":
        selected_ids = request.POST.getlist('selected_rows[]')
        # remove the ids of inflow transactions
        # that will leave the warehouse with negative stock if deleted
        deletable_ids = []
        for id in selected_ids:
            current_transaction = MODEL.objects.get(id=id)
            if current_transaction.is_inflow:
                current_stock = MODEL.get_stock(
                    current_transaction.warehouse,
                    current_transaction.item,
                )
                if current_stock - current_transaction.quantity >= 0:
                    deletable_ids.append(id)
            else:
                # outflow transaction
                deletable_ids.append(id)

        # delete all related ids in a single atomic bulk transaction
        with transaction.atomic():
            MODEL.objects.filter(id__in=deletable_ids).delete()

    return redirect(reverse(f"{APP_STR}:list_all"))

def edit_id(request, id):
    ACTION = "Editar " + VERBOSE_NAME

    # Get the address object by id
    entity = MODEL.objects.get(id=id)

    # Create the form with the address object
    if request.method == "POST":
        form = CrudForm(
            request.POST,
            instance=entity,
            crud_form_type="edit",
        )
        if form.is_valid():
            form.save()
            return redirect(reverse(f"{APP_STR}:list_all"))
    else:
        # request method is GET
        form = CrudForm(
            instance=entity,
            crud_form_type="edit",
        )
    return render(
        request, APP_STR + "/create_edit_view.html",
        {'form': form, 'action': ACTION},
    )

def list_all(request):
    ACTION = "Listar/Editar/Apagar " + VERBOSE_NAME_PLURAL
    return render(
        request,
        APP_STR + "/list.html",
        {'action': ACTION, 'table_columns': VERBOSE_COLUMN_LIST,},
    )

def list_all_api(request):
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
    for qs in queryset:
        row = []
        for col in TABLE_COLUMNS.values():
            if col in FK_FIELDS:
                # Serialize foreign key fields
                # (e.g., use their string representation or a specific field)
                fk_instance = getattr(qs, col)
                col_value = str(fk_instance) if fk_instance else None
            else:
                # Serialize regular fields
                col_value = getattr(qs, col, None)
            row.append(col_value)
        data.append(row)

    # Format JSON Response to DataTables request
    response = {
        'draw': draw,
        'recordsTotal': records_total,
        'recordsFiltered': records_filtered,
        'data': data,
    }
    return JsonResponse(response)

def view_id(request, id):
    ACTION = "Visualizar detalhes de " + VERBOSE_NAME

    # Get the entity object by id
    entity = MODEL.objects.get(id=id)

    # Create the form with the entity object
    form = CrudForm(instance=entity, crud_form_type="view")
    return render(
        request,
        APP_STR +"/create_edit_view.html",
        {'form': form, 'action': ACTION},
    )
