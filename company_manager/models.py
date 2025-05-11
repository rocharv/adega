from .validators import validate_cnpj
from django.db import models


class Company(models.Model):
    verbose_name = "Empresa"
    short_name = models.CharField(
        "Empresa",
        help_text="Use um nome curto, diferente da razão social, mas que "
        "seja único. Se o seu cadastro possuir mais de uma filial, tenha "
        "nomes diferentes para cada uma.",
        max_length=32,
        unique=True,
    )

    name = models.CharField(
        "Razão social",
        max_length=64
    )

    cnpj = models.CharField(
        "CNPJ",
        max_length=32,
        unique=True,
        validators=[validate_cnpj],
    )

    email = models.CharField(
        "Email",
        max_length=320,
        blank=True,
    )

    phone = models.CharField(
        "Telefone",
        max_length=32,
        blank=True,
    )

    website = models.CharField(
        "Website",
        max_length=64,
        blank=True,
    )

    address = models.ForeignKey(
        "address_manager.Address",
        verbose_name="Endereço",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    description = models.TextField(
        "Descrição",
        blank=True,
    )

    created_at = models.DateTimeField(
        "Criado em",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        "Atualizado em",
        auto_now=True,
    )

    def __str__(self):
        summary = self.short_name +" (" + self.cnpj + ")"
        return summary


    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ["short_name"]
        indexes = [
            models.Index(fields=["cnpj"]),
            models.Index(fields=["short_name"]),
        ]
