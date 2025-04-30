from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Button, Field, Layout, Submit
from crispy_bootstrap5.bootstrap5 import FloatingField
from .models import Address


class CrudForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"

    def __init__(self, *args, form_type ,**kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
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
        )

        # # Append crispy-forms layouts for each field
        # for field in Address._meta.get_fields():
        #     # Skip the 'id' field
        #     if field.name == "id":
        #         continue

        #     # if the model field is a CharField, set the layout to
        #     # FloatingField
        #     print(field.name)
        #     self.helper.layout.append(FloatingField(field.name))
