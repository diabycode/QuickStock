import decimal

from django.db import models

from stores.models import Store


class RepaymentRepaidBy(models.TextChoices):
    MONEY = ("money", "Espèce")
    PRODUCT = ("product", "Marchandise")
    SERVICE = ("service", "Service")


class DebtType(models.TextChoices):
    INCOMING = ('incoming', 'Entrant')
    OUTGOING = ('outgoing', 'Sortant')


class Debt(models.Model):
    person_concerned = models.CharField(max_length=150, verbose_name="Personne concernée")
    granted_date = models.DateField(verbose_name="Accordé le")
    initial_amount = models.DecimalField(verbose_name="Montant initial", max_digits=10, 
                                         decimal_places=2, default=decimal.Decimal(0.0))
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, verbose_name="Magasin", blank=True, null=True)   
    store_name = models.CharField(max_length=100, verbose_name="Magasin", null=True, blank=True)
    debt_type = models.CharField(max_length=15, choices=DebtType.choices, default=DebtType.OUTGOING, verbose_name="Type d'impayé")
    add_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return f"{self.person_concerned} : {self.granted_date.strftime('%d-%m-%Y')}"
    
    @property
    def remaining_amount(self):
        amount_paid = decimal.Decimal(0.0)
        for repayment in self.debtrepayment_set.all():
            amount_paid += repayment.amount

        return self.initial_amount - amount_paid

    @property
    def completly_repaid(self):
        return not bool(self.remaining_amount)

    @property
    def type(self) -> str:
        return "Entrant" if self.debt_type == "incoming" else "Sortant"

    @classmethod
    def get_verbose_name(cls):
        return cls._meta.verbose_name

    class Meta:
        verbose_name = "Impayé"
        verbose_name_plural = "Impayés"
        default_permissions = []
        permissions = [
            ("can_add", "Ajouter - Impayé"),
            ("can_change", "Modifier - Impayé"),
            ("can_delete", "Supprimer - Impayé"),
            ("can_view", "Voir - Impayé"),
        ]


class DebtRepayment(models.Model):
    debt = models.ForeignKey(Debt, on_delete=models.CASCADE, verbose_name="Dette remboursé")
    paid_at = models.DateTimeField(verbose_name="Date")
    amount = models.DecimalField(default=decimal.Decimal(0.0), verbose_name="Montant remboursé",
                                 max_digits=10, decimal_places=2)
    repaid_by = models.CharField(max_length=30, choices=RepaymentRepaidBy.choices, verbose_name="Payé en",
                                 default=RepaymentRepaidBy.MONEY)
    note = models.TextField(verbose_name="Note", blank=True, null=True)

    add_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return f"{self.debt.person_concerned} : {self.paid_at.strftime('%d-%m-%Y')}" 
    
    @classmethod
    def get_verbose_name(cls):
        return cls._meta.verbose_name

    class Meta:
        verbose_name = "Remboursement d'Impayé"
        verbose_name_plural = "Remboursements d'Impayé"
        default_permissions = []
        permissions = [
            ("can_add", "Ajouter - Reboursement d'Impayé"),
            ("can_change", "Modifier - Reboursement d'Impayé"),
            ("can_delete", "Supprimer - Reboursement d'Impayé"),
            ("can_view", "Voir - Reboursement d'Impayé"),
        ]
            
    @property
    def repaid_by_str(self):
        if self.repaid_by == "money":
            return "Espèce"
        if self.repaid_by == "product":
            return "Marchandise"
        if self.repaid_by == "service":
            return "Service"
        return None
    
   