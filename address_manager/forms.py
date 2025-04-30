from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Button, Field, Layout, Submit
from crispy_bootstrap5.bootstrap5 import FloatingField
from .models import Address


class CrudForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"

    def __init__(self, *args, is_view_only=False ,**kwargs):
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
        if is_view_only:
            # Disable all fields in the form
            for _field_name, field in self.fields.items():
                field.widget.attrs.update({"disabled": "disabled"})
            # Add to current layout a button to go back to list address
            self.helper.layout.append(
                ButtonHolder(
                    Button(
                        "cancel", "Voltar",
                        css_class="btn btn-primary",
                        onclick="window.location.href='/address_manager/list/'",
                    ),
                    css_class="d-grid gap-2 d-md-flex justify-content-end",
                )
            )
        else:
            # Add to current layout both buttons to submit and cancel
            self.helper.layout.append(
                ButtonHolder(
                    Submit("submit", "Confirmar", css_class="btn btn-primary"),
                    Button(
                        "cancel", "Cancelar",
                        css_class="btn btn-secondary",
                        onclick="window.location.href='/address_manager/list/'",
                    ),
                    css_class="d-grid gap-2 d-md-flex justify-content-end",
                )
            )
