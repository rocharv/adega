from django.db import models


class Category(models.Model):
    name = models.CharField(
        "Nome",
        help_text="Use um nome que descreva bem um item/produto.",
        max_length=64,
        unique=True,
    )

    brand = models.CharField(
        "Marca",
        max_length=64,
        blank=True,
    )

    model = models.CharField(
        "Modelo",
        max_length=128,
        blank=True,
    )

    color = models.CharField(
        "Cor",
        max_length=16,
        blank=True,
    )

    author = models.CharField(
        "Autor(es)",
        max_length=128,
        blank=True,
    )

    sku = models.CharField(
        "SKU",
        max_length=16,
        blank=True,
    )

    upc = models.CharField(
        "UPC",
        max_length=16,
        blank=True,
    )

    barcode = models.CharField(
        "Código de barras",
        max_length=16,
        blank=True,
    )

    weight = models.DecimalField(
        "Peso",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    weight_unit = models.CharField(
        "Unidade de peso",
        max_length=2,
        choices=[
            ("mg", "miligramas"),
            ("kg", "quilogramas"),
            ("g", "gramas"),
            ("lb", "libras"),
            ("oz", "onças"),
        ],
        default="kg",
        blank=True,
    )

    dimension_x = models.DecimalField(
        "Comprimento",
        max_digits=4,
        decimal_places=2,
        blank=True,
        null=True,
    )

    dimension_y = models.DecimalField(
        "largura",
        max_digits=4,
        decimal_places=2,
        blank=True,
        null=True,
    )

    dimension_z = models.DecimalField(
        "Profundidade",
        max_digits=4,
        decimal_places=2,
        blank=True,
        null=True,
    )

    dimension_unit = models.CharField(
        "Unidade de medida",
        max_length=2,
        choices=[
            ("mm", "milímetros"),
            ("cm", "centímetros"),
            ("m", "metros"),
            ("in", "polegadas"),
            ("ft", "pés"),
        ],
        default="cm",
        blank=True,
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
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["sku"]),
            models.Index(fields=["upc"]),
            models.Index(fields=["barcode"]),
        ]
