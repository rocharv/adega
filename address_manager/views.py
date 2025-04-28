from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import AddressForm
from .models import Address


VERBOSE_NAME = Address._meta.verbose_name.lower()
VERBOSE_NAME_PLURAL = Address._meta.verbose_name_plural.lower()

def address_create(request):
    ACTION = "Incluir " + VERBOSE_NAME
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                VERBOSE_NAME + " anterior criada(o) com sucesso."
            )
            # clear the form
            form = AddressForm()
        else:
            messages.error(
                request,
                VERBOSE_NAME + " anterior não foi criado(a)."
            )
            # return the form with errors
    else:
        form = AddressForm()
    return render(
        request, "address_manager/create_view.html",
        {'form': form, 'action': ACTION},
    )

def address_delete(request):
    ACTION = "Excluir " + VERBOSE_NAME
    # Get the address object by id
    if request.method == "POST":
        # delete all related ids
        print("Rodrigo:")
        print(request.POST.getlist('ids'))
        Address.objects.filter(id__in=request.POST.getlist('ids'))
        messages.success(
            request,
            VERBOSE_NAME + " anterior excluída(o) com sucesso."
        )
    return redirect(address_list)

def address_edit(request, id):
    ACTION = "Alterar " + VERBOSE_NAME
    # Get the address object by id
    address = Address.objects.get(id=id)
    # Create the form with the address object
    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                VERBOSE_NAME + " anterior alterado(a) com sucesso."
            )
            return redirect(address_list)
        else:
            messages.error(
                request,
                VERBOSE_NAME + " anterior não foi alterado(a)."
            )
    else:
        form = AddressForm(instance=address)
    return render(
        request, "address_manager/create_view.html",
        {'form': form, 'action': ACTION},
    )

def address_list(request):
    ACTION = "Listar/Editar/Apagar " + VERBOSE_NAME_PLURAL
    addresses = Address.objects.all()
    return render(
        request, "address_manager/list.html",
        {
            'addresses': addresses,
            'action': ACTION},
    )

def address_list_api(request):
    # --- 1. Get DataTables parameters ---
    draw = int(request.GET.get('draw', 0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')

    # --- Column mapping (MUST match your HTML table header order and models.py fields) ---
    # This maps the DataTables column index (0, 1, 2...) to your Address model field names
    # Ensure this order matches the <th> order in your HTML: Id, Logradouro, Número, Cidade, Estado, Criado em
    column_mapping = {
        0: 'id',         # Assuming you want the model's primary key as 'Id'
        1: 'street',     # Corresponds to 'Logradouro'
        2: 'number',     # Corresponds to 'Número'
        3: 'city',       # Corresponds to 'Cidade'
        4: 'state',      # Corresponds to 'Estado'
        5: 'created_at', # Corresponds to 'Criado em'
    }

    # --- Sorting ---
    order_column_index = int(request.GET.get('order[0][column]', 0))
    order_dir = request.GET.get('order[0][dir]', 'asc')
    # Get the field name from mapping, default to 'id' if index is out of bounds
    order_column_name = column_mapping.get(order_column_index, 'id')
    if order_dir == 'desc':
        order_column_name = f"-{order_column_name}"

    # --- Base QuerySet ---
    queryset = Address.objects.all() #

    # --- Total Records (before filtering) ---
    records_total = queryset.count()

    # --- Filtering (Global Search) ---
    # Adjust fields included in the search based on your model and table
    if search_value:
        search_filter = (
            Q(street__icontains=search_value) |       # Search 'Logradouro'
            Q(number__icontains=search_value) |       # Search 'Número'
            Q(city__icontains=search_value) |         # Search 'Cidade'
            Q(state__icontains=search_value) |        # Search 'Estado'
            Q(zip_code__icontains=search_value) |     # Added zip_code
            Q(neighborhood__icontains=search_value) # Added neighborhood
            # Add Q(id__icontains=search_value) if you want to search by ID,
            # but it might need conversion if search_value isn't numeric.
        )
        queryset = queryset.filter(search_filter)

    # --- Filtered Records Count ---
    records_filtered = queryset.count()

    # --- Apply Sorting and Pagination ---
    # Use `.distinct()` if your filtering involves joins that might create duplicates
    queryset = queryset.order_by(order_column_name).distinct()[start:start + length]

    # --- Prepare data for JSON response ---
    data = []
    for address in queryset:
        data.append([
            address.id,                                  # Id
            address.street,                              # Logradouro
            address.number,                              # Número
            address.city,                                # Cidade
            address.state,                               # Estado
            address.created_at.strftime('%Y-%m-%d %H:%M:%S') # Criado em
                if address.created_at else ''             # Format date safely
        ])

    # --- 5. Format JSON Response ---
    response = {
        'draw': draw,
        'recordsTotal': records_total,
        'recordsFiltered': records_filtered,
        'data': data,
    }
    return JsonResponse(response)

def address_view(request, id):
    ACTION = "Visualizar " + VERBOSE_NAME
    # Get the address object by id
    address = Address.objects.get(id=id)
    # Create the form with the address object
    form = AddressForm(instance=address, is_view_only=True)
    return render(
        request, "address_manager/create_view.html",
        {'form': form, 'action': ACTION},
    )
