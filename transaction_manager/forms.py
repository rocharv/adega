from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Button, Submit
from django import forms
from django.apps import apps
from django.db.models import DateField, DateTimeField, Model
from django.forms import DateInput, DateTimeInput
from django_select2.forms import ModelSelect2Widget
from transaction_manager.models import Transaction
## Make changes here -------------------------------------------------------
APP_STR = "transaction_manager"
MODEL_STR = "Transaction"
VIEW_ROUTE = f"/{APP_STR}/list/"


# Define all the widgets for foreign key fields
class CompanyWidget(ModelSelect2Widget):
    queryset = apps.get_model('company_manager', 'Company').objects.all()
    search_fields = [
        'short_name__icontains',
        'name__icontains',
        'cnpj__icontains',
    ]


class Html5DateInput(DateInput):
    input_type = 'date'

    def __init__(self, attrs=None, format='%Y-%m-%d'):
        super().__init__(attrs, format=format)


class ItemWidget(ModelSelect2Widget):
    queryset = apps.get_model('item_manager', 'Item').objects.all()
    search_fields = [
        'category__name__icontains',
        'corporate_tag__icontains',
        'serial_number__icontains',
    ]


class PersonWidget(ModelSelect2Widget):
    queryset = apps.get_model('person_manager', 'Person').objects.all()
    search_fields = [
        'full_name__icontains',
        'cpf__icontains',
        'email__icontains',
    ]


class WarehouseWidget(ModelSelect2Widget):
    queryset = apps.get_model('warehouse_manager', 'Warehouse').objects.all()
    search_fields = [
        'name__icontains',
        'company__name__icontains',
    ]
## -------------------------------------------------------------------------

# Get the model dynamically
try:
    MODEL: Model = apps.get_model(APP_STR, MODEL_STR)
except ImportError:
    MODEL: Model = None
    raise ImportError(
        f"Model {MODEL_STR} not found in app {APP_STR}. "
        f"Please check the model name and app name."
    )


class CrudForm(forms.ModelForm):
    class Meta:
        model = MODEL
        fields = "__all__"
        widgets = {
## Make changes here -------------------------------------------------------
            'actor': PersonWidget,
            'beginning_date': Html5DateInput,
            'company_counterpart': CompanyWidget,
            'end_date': Html5DateInput,
            'is_inflow': forms.HiddenInput,
            'item': ItemWidget,
            'person_counterpart': PersonWidget,
            'warehouse': WarehouseWidget
## -------------------------------------------------------------------------
        }

    # validate quantity to ensure it is not negative
    def clean(self):
        cleaned_data = super().clean()
        is_inflow = cleaned_data.get('is_inflow')
        item = cleaned_data.get('item')
        quantity = cleaned_data.get('quantity')
        warehouse = cleaned_data.get('warehouse')
        # Validate quantity for non-fungible items
        if item and not item.category.is_fungible:
            if quantity is None or quantity != 1:
                raise forms.ValidationError(
                    "Para itens não fungíveis, a quantidade deve ser 1.",
                    code='unitary')
        # validate warehouse to ensure there is enough stock
        # for the requested quantity

        # CrudForm type is 'edit' and the instance is outflow
        if self.instance.quantity and not self.instance.is_inflow:
            current_transaction_quantity = self.instance.quantity
        else:
            current_transaction_quantity = 0

        if warehouse and quantity and item:
            available_stock = (
                Transaction.get_stock(warehouse, item) +
                current_transaction_quantity)
            if not is_inflow and quantity > available_stock:
                raise forms.ValidationError(
                    "Não há estoque suficiente no armazém para efetuar "
                    "essa transação de saída, para esse item.",
                    code='out_of_stock',
                )
        return cleaned_data

    def __init__(self, *args, **kwargs):
        # Get the CRUD form type from the kwargs and pop it
        CRUD_FORM_TYPE = kwargs.pop("crud_form_type", None)

        # Get the TRANSACTION_TYPE from the kwargs and pop it
        TRANSACTION_TYPE = kwargs.pop("transaction_type", None)

        super().__init__(*args, **kwargs)

        # Adjust Transaction.type field based on the TRANSACTION_TYPE
        if not TRANSACTION_TYPE:
            if self.instance.is_inflow:
                TRANSACTION_TYPE = "inflow"
            else:
                TRANSACTION_TYPE = "outflow"
        print("TRANSACTION_TYPE", TRANSACTION_TYPE)
        if TRANSACTION_TYPE == "inflow":
            self.fields["is_inflow"].initial = True
            self.fields["type"].choices = [
                ("compra", "Compra"),
                ("doação (entrada)", "Doação (Entrada)"),
                ("empréstimo (entrada)", "Empréstimo (Entrada)"),
                ("retorno (entrada)", "Retorno (Entrada)"),
                ("transferência (entrada)", "Transferência (Entrada)"),
            ]
        elif TRANSACTION_TYPE == "outflow":
            self.fields["is_inflow"].initial = False
            self.fields["type"].choices = [
                ("venda", "Venda"),
                ("doação (saída)", "Doação (Saída)"),
                ("empréstimo (saída)", "Empréstimo (Saída)"),
                ("retorno (saída)", "Retorno (Saída)"),
                ("transferência (saída)", "Transferência (Saída)"),
                ("descarte", "Descarte"),
            ]

        # Set custo error for quantity field
        self.fields["quantity"].error_messages = {
            "unitary": "Para itens não fungíveis, "
                       "a quantidade deve ser 1.",
            "out_of_stock": "Não há estoque suficiente no armazém."
        }

        # Helper for crispy forms
        self.helper = FormHelper(self)
        self.helper.form_method = "POST"

        # Set the form action dynamically
        if CRUD_FORM_TYPE == "create":
            # Apply HTML5 date/datetime widgets only for 'create' form type
            for field_name, field in self.fields.items():
                # Get the model field to check its type
                model_field = MODEL._meta.get_field(field_name)
                if isinstance(model_field, DateField):
                    self.fields[field_name].widget = Html5DateInput()

            self.helper.layout.append(
                ButtonHolder(
                    Submit(
                        "submit",
                        "Incluir",
                        css_class="btn btn-primary"),
                    Button("cancel",
                           "Cancelar",
                           css_class="btn btn-secondary",
                           onclick=f"window.location.href='{VIEW_ROUTE}'"),
                           css_class=("d-grid gap-2 d-md-flex "
                            "justify-content-end"),
                )
            )
        elif CRUD_FORM_TYPE == "edit":
             self.helper.layout.append(
                 ButtonHolder(
                     Submit(
                         "submit",
                         "Salvar",
                         css_class="btn btn-primary"),
                     Button("cancel",
                            "Cancelar",
                            css_class="btn btn-secondary",
                            onclick=f"window.location.href='{VIEW_ROUTE}'"),
                           css_class=("d-grid gap-2 d-md-flex "
                            "justify-content-end"),
                 )
             )
        elif CRUD_FORM_TYPE == "view":
            for field_name in self.fields:
                self.fields[field_name].disabled = True
                self.fields[field_name].widget.attrs.update(
                    {"readonly": "readonly"})

            self.helper.layout.append(
                ButtonHolder(
                    Button("edit",
                           "Voltar",
                           css_class="btn btn-primary",
                           onclick=f"window.location.href='{VIEW_ROUTE}'"),
                           css_class=("d-grid gap-2 d-md-flex "
                            "justify-content-end"),
                )
            )
