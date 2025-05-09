from django.db import models


class Transaction(models.Model):
    INFLOW_TYPE_CHOICES = [
        ("compra", "Compra"),
        ("doação entrada", "Doação (entrada)"),
        ("empréstimo entrada", "Empréstimo (entrada)"),
        ("retorno entrada", "Retorno (entrada)"),
        ("transferência entrada", "Transferência (entrada)"),
    ]
    OUTFLOW_TYPE_CHOICES = [
        ("venda", "Venda"),
        ("doação", "Doação"),
        ("empréstimo saída", "Empréstimo (saída)"),
        ("retorno saída", "Retorno (saída)"),
        ("transferência saída", "Transferência (saída)"),
        ("descarte", "Descarte"),
    ]
    DEFAULT_TYPE_CHOICES = INFLOW_TYPE_CHOICES + OUTFLOW_TYPE_CHOICES

    warehouse = models.ForeignKey(
        "warehouse_manager.Warehouse",
        verbose_name="Armazém",
        on_delete=models.CASCADE,
        related_name="transactions"
    )

    type = models.CharField(
        "Tipo",
        max_length=32,
        choices= DEFAULT_TYPE_CHOICES,
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
        on_delete=models.SET_NULL,
        related_name="transactions",
        null=True,
        blank=True,
    )

    company_counterpart = models.ForeignKey(
        "company_manager.Company",
        verbose_name="Contraparte (empresa)",
        on_delete=models.SET_NULL,
        related_name="transactions",
        null=True,
        blank=True,
    )

    beginning_date = models.DateField(
        "Data de início",
        blank=True,
        null=True,
    )
    end_date = models.DateField(
        "Data de término",
        blank=True,
        null=True,
    )

    description = models.TextField(
        "Descrição",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        "Criado em",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        "Atualizado em",
        auto_now=True,
    )

    def get_stock(target_warehouse, target_item):
        inflow_transactions = Transaction.objects.filter(
            warehouse=target_warehouse,
            item=target_item,
            type__in=[choice[0] for choice in Transaction.INFLOW_TYPE_CHOICES]
        ).aggregate(total=models.Sum('quantity'))['total'] or 0

        outflow_transactions = Transaction.objects.filter(
            warehouse=target_warehouse,
            item=target_item,
            type__in=[choice[0] for choice in Transaction.OUTFLOW_TYPE_CHOICES]
        ).aggregate(total=models.Sum('quantity'))['total'] or 0

        return inflow_transactions - outflow_transactions

    def __str__(self):
        summary = self.warehouse.name
        summary += " - " + self.type
        summary += " - " + self.quantity
        summary += " " + self.item.category.name
        return summary


    class Meta:
        verbose_name = "Transação"
        verbose_name_plural = "Transações"
        ordering = ["created_at", "item"]
        indexes = [
            models.Index(fields=["warehouse"]),
            models.Index(fields=["type"]),
            models.Index(fields=["item"]),
            models.Index(fields=["invoice"]),
            models.Index(fields=["company_counterpart"]),
            models.Index(fields=["person_counterpart"]),
        ]
