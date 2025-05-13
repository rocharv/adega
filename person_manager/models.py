from .validators import validate_cpf
from django.db import models


class Person(models.Model):
    cpf = models.CharField(
        "CPF",
        max_length=32,
        unique=True,
        validators=[validate_cpf],
    )

    full_name = models.CharField(
        "Nome Completo",
        max_length=64,
    )

    email = models.CharField(
        "Email",
        max_length=320,
        blank=True,
    )

    rg = models.CharField(
        "RG",
        max_length=32,
        blank=True,
    )

    phone = models.CharField(
        "Telefone",
        max_length=32,
        blank=True,
    )

    company = models.ForeignKey(
        "company_manager.Company",
        verbose_name="Empresa",
        on_delete=models.CASCADE,
        related_name="people",
        blank=True,
        null=True,
    )

    address = models.ForeignKey(
        "address_manager.Address",
        verbose_name="Endereço Residencial",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    birthdate = models.DateField(
        "Data de Nascimento",
        blank=True,
        null=True
    )

    comment = models.TextField(
        "Comentário",
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
        summary = self.full_name + " (" + self.cpf + ")"
        return summary


    class Meta:
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"
        ordering = ["full_name"]
        indexes = [
            models.Index(fields=["cpf"]),
            models.Index(fields=["full_name"]),
        ]
