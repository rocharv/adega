from django.db import models


class Transaction(models.Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.transaction_type = kwargs.get("transaction_type", None)
        if self.transaction_type == 'outflow':
            TYPE_CHOICES = [
                ("sale", "Venda"),
                ("donation", "Doação"),
                ("lent", "Empréstimo"),
                ("return", "Devolução"),
                ("transfer", "Transferência"),
                ("waste", "Descarte"),
            ]
        TYPE_CHOICES = [
            ("purchase", "Compra"),
            ("donation", "Doação"),
            ("borrow", "Empréstimo"),
            ("return", "Retorno"),
            ("transfer", "Transferência"),
        ]

        warehouse = models.ForeignKey(
            "warehouse_manager.Warehouse",
            verbose_name="Armazém",
            on_delete=models.CASCADE,
            related_name="transactions"
        )

        type = models.CharField(
            "Tipo de saída",
            max_length=32,
            choices= TYPE_CHOICES,
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
