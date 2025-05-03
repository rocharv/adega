from django import forms
from django.apps import apps
from django.db.models import Model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Button, Div, Field, Layout, Submit
from crispy_bootstrap5.bootstrap5 import FloatingField


# Make changes here -----------------
APP_STR = "company_manager"
MODEL_STR = "Company"
# -----------------------------------
VIEW_ROUTE = f"/{APP_STR}/list/"
try:
    MODEL: Model = apps.get_model(APP_STR, MODEL_STR)

except ImportError:
    MODEL: Model = None
    raise ImportError(
        f"Model {MODEL_STR} not found in app {APP_STR}. "
        f"Please check the model name and app name."
    )


class ModelDataForm(forms.ModelForm):
    class Meta:
        model = MODEL
        fields = "__all__"


class CrudForm(ModelDataForm):
    def __init__(self, *args, crud_form_type="create" ,**kwargs):
        super().__init__(*args, **kwargs)

        #
        primary_key = self.instance.pk

        # Set the form action based on the crud_form_type
        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.form_id = "crud-form"
        self.helper.form_class = "form-floating"

        # Set layout for the form
        self.helper.layout = Layout()
        for field in self.fields:
            if isinstance(self.fields[field], forms.ChoiceField):
                # Use browser default select picker
                self.helper.layout.append(
                    Field(
                        field,
                    ),
                    css_class="width: 100%; height: 2rem",
                )
            elif isinstance(self.fields[field], forms.DateField):
                # Use browser default date picker
                self.fields[field].widget.attrs.update(
                    {
                        "type": "date",
                        "class": "form-control",
                    }
                )
            elif isinstance(self.fields[field], forms.DateTimeField):
                # Use browser default datetime picker
                self.fields[field].widget.attrs.update(
                    {
                        "type": "datetime-local",
                        "class": "form-control",
                    }
                )
            else:
                self.helper.layout.append(
                    FloatingField(field)
                )

        # Add buttons and layout details according to the crud_form_type
        if crud_form_type == "create":
            # Add buttons to create and cancel
            self.helper.layout.append(
                ButtonHolder(
                    Submit("submit", "Incluir", css_class="btn btn-primary"),
                    Button(
                        "cancel",
                        "Cancelar",
                        css_class="btn btn-secondary",
                        onclick=f"window.location.href='{VIEW_ROUTE}'",
                    ),
                    css_class="d-grid gap-2 d-md-flex justify-content-end",
                )
            )
        elif crud_form_type == "edit":
            # Add buttons to save and cancel
            self.helper.layout.append(
                ButtonHolder(
                    Submit("submit", "Salvar", css_class="btn btn-primary"),
                    Button(
                        "cancel",
                        "Cancelar",
                        css_class="btn btn-secondary",
                        onclick=f"window.location.href='{VIEW_ROUTE}'",
                    ),
                    css_class="d-grid gap-2 d-md-flex justify-content-end",
                )
            )
        elif crud_form_type == "view":
            # Disable all fields in view mode
            for field in self.fields:
                self.fields[field].disabled = True
                self.fields[field].widget.attrs.update(
                    {"readonly": "readonly"}
                )
            # Add a button to go back to the list view
            self.helper.layout.append(
                ButtonHolder(
                    Button(
                        "edit",
                        "Voltar",
                        css_class="btn btn-primary",
                        onclick=f"window.location.href='{VIEW_ROUTE}'",
                    ),
                    css_class="d-grid gap-2 d-md-flex justify-content-end",
                )
            )
