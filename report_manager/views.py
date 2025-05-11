from django.db.models import F, Q
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Case, When, IntegerField, Sum
from transaction_manager.models import Transaction


# Report queryset: stock by category
# This queryset aggregates the stock of items by category and warehouse.
REPORT_BY_CATEGORY = Transaction.objects.values(
    warehouse_name=F("warehouse__name"),
    item_category_name=F("item__category__name"),
).annotate(
    item_quantity=Sum(
        Case(
            When(is_inflow=True, then=F("quantity")),
            When(is_inflow=False, then=-F("quantity")),
            output_field=IntegerField(),
        )
    )
).order_by("warehouse_name", "item_category_name")

# Report queryset: stock by items
# This queryset aggregates the stock of items by item name, corporate tag,
# item serial number and warehouse.
REPORT_BY_ITEM = Transaction.objects.values(
    warehouse_name=F("warehouse__name"),
    item_name=F("item__category__name"),
    corporate_tag=F("item__corporate_tag"),
    serial_number=F("item__serial_number"),
).annotate(
    item_quantity=Sum(
        Case(
            When(is_inflow=True, then=F("quantity")),
            When(is_inflow=False, then=-F("quantity")),
            output_field=IntegerField(),
        )
    )
).order_by("warehouse_name", "item_name")


def list_by(request, list_type: str):
    if list_type == "category":
        template = "report_manager/report_by_category.html"
        action = "Relatório de Estoque por Categoria"
        verbose_column_list = [
            "Nome do Armazém",
            "Quantidade de Itens",
            "Nome da Categoria",
        ]
    elif list_type == "item":
        template = "report_manager/report_by_item.html"
        action = "Relatório de Estoque por Itens"
        verbose_column_list = [
            "Nome do Armazém",
            "Quantidade de Itens",
            "Nome do Item",
            "Etiqueta de Patrimônio",
            "Número de Série",
        ]

    return render(
        request,
        template,
        {'action': action, 'table_columns': verbose_column_list,},
    )


def list_by_api(request, list_type: str):
    """
    Return the report as a JSON usable by the DataTable API.
    """
    # Base QuerySet acording to the list_type
    if list_type == "item":
        queryset = REPORT_BY_ITEM
        queryset_columns = [
            "warehouse_name",
            "item_quantity",
            "item_name",
            "corporate_tag",
            "serial_number",
        ]
    elif list_type == "category":
        queryset = REPORT_BY_CATEGORY
        queryset_columns = [
            "warehouse_name",
            "item_quantity",
            "item_category_name",
        ]

    # Get DataTables parameters
    draw = int(request.GET.get('draw', 0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')
    order_column_index = int(request.GET.get('order[0][column]', 0))
    order_dir = request.GET.get('order[0][dir]', 'asc')

    # Get the field name from mapping,
    # default to 'id' if index is out of bounds
    if order_column_index < len(queryset_columns):
        order_column_name = queryset_columns[order_column_index]
    else:
        order_column_name = 'id'

    if order_dir == 'desc':
        order_column_name = f"-{order_column_name}"

    # Total records count before filtering
    records_total = queryset.count()
    # Filter the queryset by search value
    if search_value:
        if list_type == "item":
            queryset = queryset.filter(
                Q(warehouse_name__icontains=search_value) |
                Q(item_name__icontains=search_value)
            )
        elif list_type == "category":
            # Filter by category name
            queryset = queryset.filter(
                Q(warehouse_name__icontains=search_value) |
                Q(item_category_name__icontains=search_value)
            )
    # Filtered records count
    records_filtered = queryset.count()
    # Apply ordering
    queryset = queryset.order_by(order_column_name).distinct()[start:start + length]
    # Prepare data field for JSON response to DataTables
    data = []
    for row in queryset:
        data.append([str(row[column]) for column in queryset_columns])
    # Prepare the JSON response
    response = {
        'draw': draw,
        'recordsTotal': records_total,
        'recordsFiltered': records_filtered,
        'data': data,
    }
    return JsonResponse(response)
