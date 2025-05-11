from django import forms
from django.apps import apps
from django.db.models import DateField, DateTimeField, Model
from django.forms import DateInput, DateTimeInput
from django_select2.forms import ModelSelect2Widget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Button, Submit

## Make changes here -------------------------------------------------------
APP_STR = "person_manager"
MODEL_STR = "Person"
VIEW_ROUTE = f"/{APP_STR}/list/"

# Define all the widgets for foreign key fields
class AddressWidget(ModelSelect2Widget):
    queryset = apps.get_model('address_manager', 'Address').objects.all()
    search_fields = [
        'zip_code__icontains',
        'street__icontains',
        'number__icontains',
        'complement__icontains',
        'neighborhood__icontains',
        'city__icontains',
        'state__icontains',
        'country__icontains',
    ]

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs.update({'class': 'form-control', 'type': 'date'})


class CompanyWidget(ModelSelect2Widget):
    queryset = apps.get_model('company_manager', 'Company').objects.all()
    search_fields = [
        'short_name__icontains',
        'name__icontains',
        'cnpj__icontains',
    ]
## -------------------------------------------------------------------------

# Define the HTML5 date and datetime widgets
class Html5DateInput(DateInput):
    input_type = 'date'

    def __init__(self, attrs=None, format='%Y-%m-%d'):
        super().__init__(attrs, format=format)

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
            'address': AddressWidget,
            'company': CompanyWidget,
            'birthdate': Html5DateInput,
## -------------------------------------------------------------------------
        }

    def __init__(self, *args, crud_form_type="create" ,**kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = "POST"

        if crud_form_type == "create":
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
        elif crud_form_type == "edit":
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
        elif crud_form_type == "view":
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
