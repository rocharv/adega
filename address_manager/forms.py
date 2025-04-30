from django import forms
from django.apps import apps
from django.db.models import Model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Button, Field, Layout, Submit
from crispy_bootstrap5.bootstrap5 import FloatingField

from  .models import Address

# Make changes here -----------------
APP_STR = "address_manager"
MODEL_STR = "Address"
# -----------------------------------

VIEW_ROUTE = f"/{APP_STR}/list/"

try:
    FORM_MODEL: Model = apps.get_model(APP_STR, MODEL_STR)
except ImportError:
    FORM_MODEL: Model = None
    raise ImportError(
        f"Model {MODEL_STR} not found in app {APP_STR}. "
        f"Please check the model name and app name."
    )


class CrudForm(forms.ModelForm):
    class Meta:
        model = FORM_MODEL
        fields = "__all__"

    def __init__(self, *args, crud_form_type="create" ,**kwargs):
        super().__init__(*args, **kwargs)

        # Set atributte helper to crispy-forms FormHelper
        self.helper = FormHelper()

        # Set the form tag attributes and avoid browser validation
        self.helper.form_class = 'form-floating'
        self.helper.form_method = 'post'
        self.helper.attrs = {
            "novalidate": "novalidate",
        }

        # Set Layout to crispy-forms Layout
        self.helper.layout = Layout()
        for field_name in self.fields:
            # if field type is DateField, set widget to HTML 5 date input
            if isinstance(self.fields[field_name], forms.DateField):
                self.fields[field_name].widget.input_type = "date"
            else:
                self.helper.layout.fields.append(FloatingField(field_name))

        # Add placeholders to all fields and disable them if is_view_only
        for _field_name, field in self.fields.items():
            field.widget.attrs.update({"placeholder": field.label})
        if crud_form_type == "view":
            # Disable all fields in the form
            for _field_name, field in self.fields.items():
                field.widget.attrs.update({"disabled": "disabled"})
            # Add to current layout a button to go back to list address
            self.helper.layout.append(
                ButtonHolder(
                    Button(
                        "cancel", "Voltar",
                        css_class="btn btn-primary",
                        onclick="window.location.href='" + VIEW_ROUTE + "'",
                    ),
                    css_class="d-grid gap-2 d-md-flex justify-content-end",
                )
            )
        if crud_form_type == "create":
            # Add to current layout both buttons to submit and cancel
            # create returns to the same page to facilitate multiple inputs
            self.helper.layout.append(
                ButtonHolder(
                    Submit("submit", "Confirmar", css_class="btn btn-primary"),
                    Button(
                        "cancel", "Cancelar",
                        css_class="btn btn-secondary",
                        onclick="window.location.href='" + VIEW_ROUTE + "'",
                    ),
                    css_class="d-grid gap-2 d-md-flex justify-content-end",
                )
            )
        if crud_form_type == "edit":
            # Add to current layout both buttons to submit and cancel
            # edit returns to list
            self.helper.layout.append(
                ButtonHolder(
                    Submit("submit", "Confirmar", css_class="btn btn-primary"),
                    Button(
                        "cancel", "Cancelar",
                        css_class="btn btn-secondary",
                        onclick="window.location.href='" + VIEW_ROUTE + "'",
                    ),
                    css_class="d-grid gap-2 d-md-flex justify-content-end",
                )
            )
