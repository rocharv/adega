from django.db import models


class Item(models.Model):
    category = models.ForeignKey(
        "category_manager.Category",
        verbose_name="Categoria",
        on_delete=models.CASCADE,
        related_name="items",
    )

    corporate_tag = models.CharField(
        "Etiqueta de Patrimônio", max_length=32,
        help_text=(
            "Número que identifica exclusivamente um item dentro de uma "
            "empresa ou instituição. Exemplo: 123456, 1234-5678, etc."
            ),
        blank=True
    )

    serial_number = models.CharField(
        "Número de Série", max_length=32,
        help_text=(
            "Número que identifica exclusivamente um item. Por exemplo: "
            "o IMEI de um celular, o número de série de um computador, etc."
            ),
        blank=True
    )

    is_new = models.BooleanField(
        "novo (marque se o item nunca foi usado anteriormente)",
        default=True,
        blank=True
    )

    description = models.TextField(
        "Descrição",
        blank=True,
    )

    created_at = models.DateTimeField(
        "Criado em",
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        "Atualizado em",
        auto_now=True
    )

    def __str__(self):
        summary = self.category.name
        if self.corporate_tag:
            summary += " - etiqueta: " + self.corporate_tag
        if self.serial_number:
            summary += f" - n/s: " + self.serial_number
        return summary


    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"
        ordering = ["category", "corporate_tag"]
        indexes = [
            models.Index(fields=["corporate_tag"]),
            models.Index(fields=["serial_number"]),
            models.Index(fields=["category"]),
        ]
