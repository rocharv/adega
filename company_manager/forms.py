# company_manager/forms.py

from django import forms
from django.apps import apps
from django.db.models import Model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Button, Layout, Submit, Field
from crispy_bootstrap5.bootstrap5 import FloatingField
# Import the select2 widget
from django_select2.forms import ModelSelect2Widget

# Your existing code
APP_STR = "company_manager"
MODEL_STR = "Company"
VIEW_ROUTE = f"/{APP_STR}/list/"
try:
    MODEL: Model = apps.get_model(APP_STR, MODEL_STR)
except ImportError:
    MODEL: Model = None
    raise ImportError(
        f"Model {MODEL_STR} not found in app {APP_STR}. "
        f"Please check the model name and app name."
    )

# Define the widget for the address field
class AddressWidget(ModelSelect2Widget):
    # Define the queryset for the Address model
    # Ensure 'address_manager.Address' matches your actual app and model name
    queryset = apps.get_model('address_manager', 'Address').objects.all()
    search_fields = [
        # Add fields from Address model to search against
        # Example: Assuming Address model has 'street', 'city', 'zip_code' fields
        'street__icontains',
        'city__icontains',
        'zip_code__icontains',
        # Add other relevant fields from the Address model
    ]


class CrudForm(forms.ModelForm):
    class Meta:
        model = MODEL
        fields = "__all__"
        # Assign the custom widget to the 'address' field
        widgets = {
            'address': AddressWidget,
        }

    def __init__(self, *args, crud_form_type="create" ,**kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = "POST"

        # Add buttons based on crud_form_type (Your existing logic)
        if crud_form_type == "create":
            self.helper.layout.append(
                ButtonHolder(
                    Submit("submit", "Incluir", css_class="btn btn-primary"),
                    Button("cancel", "Cancelar", css_class="btn btn-secondary", onclick=f"window.location.href='{VIEW_ROUTE}'"),
                    css_class="d-grid gap-2 d-md-flex justify-content-end",
                )
            )
        elif crud_form_type == "edit":
             self.helper.layout.append(
                 ButtonHolder(
                     Submit("submit", "Salvar", css_class="btn btn-primary"),
                     Button("cancel", "Cancelar", css_class="btn btn-secondary", onclick=f"window.location.href='{VIEW_ROUTE}'"),
                     css_class="d-grid gap-2 d-md-flex justify-content-end",
                 )
             )
        elif crud_form_type == "view":
            for field_name in self.fields:
                self.fields[field_name].disabled = True
                self.fields[field_name].widget.attrs.update({"readonly": "readonly"})

            self.helper.layout.append(
                ButtonHolder(
                    Button("edit", "Voltar", css_class="btn btn-primary", onclick=f"window.location.href='{VIEW_ROUTE}'"),
                    css_class="d-grid gap-2 d-md-flex justify-content-end",
                )
            )

        # Ensure the select2 media is included when rendering the form
        # self.helper.include_media = True # Crucial for including JS/CSS
