from django.db import models


class Transaction(models.Model):
    warehouse = models.ForeignKey(
        "warehouse_manager.Warehouse",
        verbose_name="Armazém",
        on_delete=models.CASCADE,
        related_name="transactions"
    )

    DEFAULT_TYPE_CHOICES = [
        ("compra", "Compra"),
        ("venda", "Venda"),
        ("doação", "Doação"),
        ("empréstimo", "Empréstimo"),
        ("retorno", "Retorno"),
        ("transferência", "Transferência"),
        ("descarte", "Descarte"),
    ]
    type = models.CharField(
        "Tipo",
        max_length=32,
        choices= DEFAULT_TYPE_CHOICES,
        default="compra",
    )

    is_inflow = models.BooleanField(
        "Operação de entrada",
        default=True,
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

    actor = models.ForeignKey(
        "person_manager.Person",
        verbose_name="Pessoa que executou a transação",
        on_delete=models.SET_NULL,
        related_name="transactions_actor",
        null=True,
        blank=True,
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
           is_inflow=True,
        ).aggregate(total=models.Sum('quantity'))['total'] or 0

        outflow_transactions = Transaction.objects.filter(
            warehouse=target_warehouse,
            item=target_item,
            is_inflow=False,
        ).aggregate(total=models.Sum('quantity'))['total'] or 0

        return inflow_transactions - outflow_transactions

    def __str__(self):
        summary = self.warehouse.name
        summary += " - " + self.type
        summary += " - " + str(self.quantity)
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
