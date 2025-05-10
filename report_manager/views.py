from django.db.models import F, Q
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Sum
from transaction_manager.models import Transaction


# Report queryset: stock by category
# This queryset aggregates the stock of items by category and warehouse.
report_by_category = Transaction.objects.values(
    warehouse_name=F("warehouse__name"),
    item_category_name=F("item__category__name"),
).annotate(
    item_quantity=Sum(
        F("quantity") * (1 if F("is_inflow") else -1)
    )
).order_by("warehouse_name", "item_category_name")



def list_by_category(request):
    ACTION = "Relatório de Estoque por Categoria"
    VERBOSE_COLUMN_LIST = [
        "Nome do Armazém",
        "Quantidade de Itens",
        "Nome da Categoria",
    ]
    return render(
        request,
        "report_manager/list.html",
        {'action': ACTION, 'table_columns': VERBOSE_COLUMN_LIST,},
    )

def list_all_api(request):
    # debugging report
    print(report_by_category.query)
    for row in report_by_category:
        print(row)

    """
    Return the report as a JSON usable by the DataTable API.
    """

    # Get DataTables parameters
    draw = int(request.GET.get('draw', 0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')
    order_column_index = int(request.GET.get('order[0][column]', 0))
    order_dir = request.GET.get('order[0][dir]', 'asc')
    # Get the field name from mapping,
    # default to 'id' if index is out of bounds
    order_column_name = [
        "warehouse_name",
        "item_quantity",
        "item_category_name",
    ][order_column_index] if order_column_index < 3 else 'id'
    if order_dir == 'desc':
        order_column_name = f"-{order_column_name}"
    # Base QuerySet
    queryset = report_by_category
    # Total records count before filtering
    records_total = queryset.count()
    # Filter the queryset by search value
    if search_value:
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
    for item in queryset:
        data.append([
            item["warehouse_name"],
            item["item_quantity"],
            item["item_category_name"],
        ])
    # Prepare the JSON response
    response = {
        'draw': draw,
        'recordsTotal': records_total,
        'recordsFiltered': records_filtered,
        'data': data,
    }
    return JsonResponse(response)
