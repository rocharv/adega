# forms.py
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label="Usuário",
        widget=forms.TextInput(attrs={"placeholder": "Usuário"})
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"placeholder": "Senha"})
    )

    def __init__(self, *args, **kwargs):
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
            FloatingField("username"),
            FloatingField("password"),
        )
        self.helper.add_input(Submit("submit", "Login", css_class="w-100"))
