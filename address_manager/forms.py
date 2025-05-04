from django import forms
from django.apps import apps
from django.db.models import Model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Button, Submit


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
