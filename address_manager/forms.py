from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Button, Field, Layout, Submit
from crispy_bootstrap5.bootstrap5 import FloatingField
from .models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

    def __init__(self, *args, is_view_only=False ,**kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # Set the form tag attributes
        self.helper.form_class = 'form-floating'
        self.helper.form_method = 'post'
        self.helper.attrs = {
            "novalidate": "novalidate",
        }
        # Set the layout of the form
        self.helper.layout = Layout(
            FloatingField("zip_code"),
            FloatingField("street"),
            FloatingField("number"),
            FloatingField("complement"),
            FloatingField("neighborhood"),
            FloatingField("city"),
            FloatingField("state"),
            FloatingField("country"),
            FloatingField("reference"),
            # ButtonHolder(
            #     Submit("submit", "Incluir", css_class="btn btn-primary"),
            #     Button(
            #         "cancel", "Cancelar",
            #         css_class="btn btn-secondary",
            #         onclick="window.location.href='/'",
            #     ),
            # ),
        )
        # Special case for the 'birthdate' field: set type to 'date'
        # This is necessary because the default widget for DateInput is 'text'
        # in Django, and we want to use the HTML5 date input type
        self.fields["reference"].widget = forms.Textarea(
            attrs={
                "style": "height: 10rem",
            }
        )
        # Add placeholders to all fields and disable them if is_view_only
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"placeholder": field.label})
        # Set the label for the 'company' field to show the short name
        # instead of the default string representation
        # self.fields["company"].label_from_instance = lambda obj: obj.short_name
        # # change action to return to "/person/list/" in case of is_view_only
        if is_view_only:
            # Disable all fields in the form
            for field_name, field in self.fields.items():
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
