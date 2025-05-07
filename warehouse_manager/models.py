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


class InflowTransaction(models.Model):
    warehouse = models.ForeignKey(
        Warehouse,
        verbose_name="Armazém",
        on_delete=models.CASCADE,
        related_name="inflows"
    )

    type = models.CharField(
        "Tipo de entrada",
        max_length=32,
        choices=[
            ("purchase", "Compra"),
            ("donation", "Doação"),
            ("borrow", "Empréstimo"),
            ("return", "Retorno"),
            ("transfer", "Transferência"),
        ],
        default="purchase",
    )

    invoice = models.CharField(
        "Nota fiscal ou recibo",
        max_length=32,
        blank=True,
        help_text=(
            "Procure usar exatamente o mesmo valor para todos os itens "
            "que estão na mesma nota fiscal ou recibo."
        ),
        null=True,
    )

    quantity = models.PositiveIntegerField(
        "Quantidade",
        default=1
    )

    item = models.ForeignKey(
        "item_manager.Item",
        verbose_name="Item",
        on_delete=models.CASCADE,
        related_name="inflows"
    )

    price = models.DecimalField(
        "Preço",
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )

    person_counterpart = models.ForeignKey(
        "person_manager.Person",
        verbose_name="Contraparte (pessoa)",
        on_delete=models.CASCADE,
        related_name="inflows"
    )

    company_counterpart = models.ForeignKey(
        "company_manager.Company",
        verbose_name="Contraparte (empresa)",
        on_delete=models.CASCADE,
        related_name="inflows"
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
        summary = self.warehouse.name
        summary += " - " + self.type
        summary += " - " + self.quantity
        summary += " " + self.item.category.name
        return summary


    class Meta:
        verbose_name = "Entrada"
        verbose_name_plural = "Entradas"
        ordering = ["created_at", "item"]
        indexes = [
            models.Index(fields=["warehouse"]),
            models.Index(fields=["item"]),
            models.Index(fields=["company_counterpart"]),
            models.Index(fields=["person_counterpart"]),
        ]


class OutflowTransaction(models.Model):
    warehouse = models.ForeignKey(
        Warehouse,
        verbose_name="Armazém",
        on_delete=models.CASCADE,
        related_name="outflows"
    )

    type = models.CharField(
        "Tipo de saída",
        max_length=32,
        choices=[
            ("sale", "Venda"),
            ("donation", "Doação"),
            ("lent", "Empréstimo"),
            ("return", "Devolução"),
            ("transfer", "Transferência"),
            ("waste", "Descarte"),
        ],
        default="sale",
    )
    invoice = models.CharField(
        "Nota fiscal ou recibo",
        max_length=32,
        blank=True,
        help_text=(
            "Procure usar exatamente o mesmo valor para todos os itens "
            "que estão na mesma nota fiscal ou recibo."
        ),
        null=True,
    )

    quantity = models.PositiveIntegerField(
        "Quantidade",
        default=1
    )

    item = models.ForeignKey(
        "item_manager.Item",
        verbose_name="Item",
        on_delete=models.CASCADE,
        related_name="outflows"
    )

    price = models.DecimalField(
        "Preço",
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )

    person_counterpart = models.ForeignKey(
        "person_manager.Person",
        verbose_name="Contraparte (pessoa)",
        on_delete=models.CASCADE,
        related_name="outflows"
    )

    company_counterpart = models.ForeignKey(
        "company_manager.Company",
        verbose_name="Contraparte (empresa)",
        on_delete=models.CASCADE,
        related_name="outflows"
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
        summary = self.warehouse.name
        summary += " - " + self.type
        summary += " - " + self.quantity
        summary += " " + self.item.category.name
        return summary


    class Meta:
        verbose_name = "Saída"
        verbose_name_plural = "Saídas"
        ordering = ["created_at", "item"]
        indexes = [
            models.Index(fields=["warehouse"]),
            models.Index(fields=["item"]),
            models.Index(fields=["company_counterpart"]),
            models.Index(fields=["person_counterpart"]),
        ]
