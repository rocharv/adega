from django.db import models


class Warehouse(models.Model):
    name = models.CharField(
        "Nome",
        help_text="Use um nome curto, único, que descreva bem o local.",
        max_length=64,
        unique=True,
    )

    company = models.ForeignKey(
        "company_manager.Company",
        verbose_name="Empresa",
        on_delete=models.CASCADE,
        related_name="warehouses"
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
        summary = self.name
        return summary


    class Meta:
        verbose_name = "Armazém"
        verbose_name_plural = "Armazéns"
        ordering = ["name", "description"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["company"]),
        ]
