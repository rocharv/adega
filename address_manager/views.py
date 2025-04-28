from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import AddressForm
from .models import Address


VERBOSE_NAME = Address._meta.verbose_name.lower()
VERBOSE_NAME_PLURAL = Address._meta.verbose_name_plural.lower()

def address_create(request):
    ACTION = "Incluir " + VERBOSE_NAME
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                VERBOSE_NAME + " anterior criada(o) com sucesso."
            )
            # clear the form
            form = AddressForm()
        else:
            messages.error(
                request,
                VERBOSE_NAME + " anterior não foi criada(o)."
            )
            # return the form with errors
    else:
        form = AddressForm()
    return render(
        request, "address_manager/create_view.html",
        {'form': form, 'action': ACTION},
    )

def address_delete(request, id):
    pass

def address_edit(request, id):
    pass

def address_list(request):
    ACTION = "Visualizar " + VERBOSE_NAME_PLURAL
    return render(
        request, "address_manager/list.html",
        {'action': ACTION},
    )

def address_view(request, id):
    ACTION = "Visualizar " + VERBOSE_NAME
    # Get the address object by id
    address = Address.objects.get(id=id)
    # Create the form with the address object
    form = AddressForm(instance=address, is_view_only=True)
    return render(
        request, "address_manager/create_view.html",
        {'form': form, 'action': ACTION},
    )
