from django import forms
from django.apps import apps
from django.db.models import DateField, DateTimeField, Model
from django.forms import DateInput, DateTimeInput
from django_select2.forms import ModelSelect2Widget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Button, Submit

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
        'company__icontains',
    ]
## -------------------------------------------------------------------------


# Define the HTML5 date and datetime widgets
class Html5DateInput(DateInput):
    input_type = 'date'


class Html5DateTimeInput(DateTimeInput):
    input_type = 'datetime-local'


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
            'beginning_date': Html5DateInput(),
            'company': CompanyWidget,
            'end_date': Html5DateInput(),
            'person': PersonWidget,
## -------------------------------------------------------------------------
        }

    def __init__(self, *args, **kwargs):
        # Get the CRUD form type from the kwargs and pop it
        CRUD_FORM_TYPE = kwargs.pop("crud_form_type", None)

        # Get the TRANSACTION_TYPE from the kwargs and pop it
        TRANSACTION_TYPE = kwargs.pop("transaction_type", None)

        super().__init__(*args, **kwargs)

        # Adjust Transaction.type field based on the TRANSACTION_TYPE
        if TRANSACTION_TYPE == "inflow":
            self.fields["type"].choices = [
                ("purchase", "Compra"),
                ("donation", "Doação"),
                ("borrow", "Empréstimo"),
                ("return", "Retorno"),
                ("transfer", "Transferência"),
            ]
        elif TRANSACTION_TYPE == "outflow":
            self.fields["type"].choices = [
                ("sale", "Venda"),
                ("donation", "Doação"),
                ("lent", "Empréstimo"),
                ("return", "Devolução"),
                ("transfer", "Transferência"),
                ("waste", "Descarte"),
            ]

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
                elif isinstance(model_field, DateTimeField):
                    self.fields[field_name].widget = Html5DateTimeInput()

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
