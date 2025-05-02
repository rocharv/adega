from django import forms
from django.apps import apps
from django.db.models import Model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Button, Field, Layout, Submit
from crispy_bootstrap5.bootstrap5 import FloatingField


# Make changes here -----------------
APP_STR = "company_manager"
MODEL_STR = "Company"
# -----------------------------------

VIEW_ROUTE = f"/{APP_STR}/list/"

try:
    FORM_MODEL: Model = apps.get_model(APP_STR, MODEL_STR)
    # Create a list of foreign key fields in FORM_MODEL
    FOREIGN_KEY_FIELDS = [
        field.name for field in FORM_MODEL._meta.get_fields()
        if field.is_relation and field.many_to_one
    ]
except ImportError:
    FORM_MODEL: Model = None
    raise ImportError(
        f"Model {MODEL_STR} not found in app {APP_STR}. "
        f"Please check the model name and app name."
    )


class ModelDataForm(forms.ModelForm):
    class Meta:
        model = FORM_MODEL
        fields = "__all__"
        exclude = FOREIGN_KEY_FIELDS


class CrudForm(ModelDataForm):
    def __init__(self, *args, primary_key=None, crud_form_type="create" ,**kwargs):
        super().__init__(*args, **kwargs)

        # Create new fields for each FOREIGN_KEY_FIELDS
        # using use forms.CharField, the initial value will be the
        # the value that comes from related model of the foreign key
        # field
        for field_name in FOREIGN_KEY_FIELDS:
            print("FK field name: ",field_name)
            # get the related model of the foreign key field
            # related_model = getattr(FORM_MODEL, field_name).related_model
            # get the instance of the FORM_MODEL
            form_model_instance = FORM_MODEL.objects.get(pk=primary_key)
            print("form_model_instance: ", form_model_instance)
            fk_instance = getattr(form_model_instance, field_name)
            print("fk_instance: ", fk_instance)
            fk_fields = fk_instance._meta.get_fields()
            for fk_field in fk_fields:
                # skip more relations
                if fk_field.is_relation:
                    continue
                fk_field_value = getattr(fk_instance, fk_field.name)
                print("fk_fields: ", fk_field, fk_field_value)

                self.fields[fk_field.name] = forms.CharField(
                    label=fk_instance.verbose_name + " - " + fk_field.verbose_name,
                    initial=fk_field_value,
                    required=False,
                )



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
        for field_name in self.fields.keys():
            # skip id
            if field_name == "id":
                continue
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
            # Add to current layout a button to go back to list
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
