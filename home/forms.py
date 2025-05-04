# forms.py
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
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
        self.helper = FormHelper(self)
        self.helper.form_method = "POST"

        # Set the layout of the form
        self.helper.layout.append(
            Submit("submit", "Login", css_class="w-100 mt-4"),
        )
