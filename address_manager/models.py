from django.db import models


class Address(models.Model):
    verbose_name = "Endereço"
    zip_code = models.CharField(
        "CEP",
        max_length=16,
    )

    street = models.CharField(
        "Logradouro",
        max_length=64,
    )

    number = models.CharField(
        "Número",
        max_length=8,
        blank=True,
    )

    complement = models.CharField(
        "Complemento",
        max_length=32,
        blank=True,
    )

    neighborhood = models.CharField(
        "Bairro",
        max_length=32,
    )

    city = models.CharField(
        "Cidade",
        max_length=64,
    )

    state = models.CharField(
        "Estado",
        max_length=64,
    )

    country = models.CharField(
        "País",
        max_length=64,
        default="Brasil",
    )

    reference = models.TextField(
        "Referência",
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
        summary = (
            f"{self.street}, {self.number + ', ' if self.number else ''}"
            f"{self.complement + ', ' if self.complement else ''}"
            f"{self.city}/{self.state}, {self.country}"
        )
        return summary


    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"
        ordering = ["zip_code", "street", "number"]
        indexes = [
            models.Index(fields=["zip_code"]),
        ]
