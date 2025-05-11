# forms.py
from crispy_forms.helper import FormHelper
from crispy_forms.layout import  Button, ButtonHolder, Layout, Submit
from django import forms
from django.contrib.auth.models import User


class ChangePasswordForm(forms.ModelForm):
    old_password = forms.CharField(
        label="Senha Antiga",
        widget=forms.PasswordInput(attrs={"placeholder": "Senha Antiga"})
    )
    new_password = forms.CharField(
        label="Nova Senha",
        widget=forms.PasswordInput(attrs={"placeholder": "Nova Senha"})
    )
    confirm_password = forms.CharField(
        label="Confirmar Senha",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirmar Senha"})
    )

    class Meta:
        model = User
        fields = ["old_password", "new_password", "confirm_password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Crispy Forms Helper and Form Method
        self.helper = FormHelper()
        self.helper.form_method = "POST"

        # Define the layout of the form
        self.helper.layout = Layout(
            "old_password",
            "new_password",
            "confirm_password",
            ButtonHolder(
                Submit(
                    "submit",
                    "Alterar Senha",
                    css_class="btn btn-primary"),
                Button("cancel",
                        "Cancelar",
                        css_class="btn btn-secondary",
                        onclick="window.location.href='/'"),
                        css_class=("d-grid gap-2 d-md-flex "
                        "justify-content-end"),
            )
        )


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
