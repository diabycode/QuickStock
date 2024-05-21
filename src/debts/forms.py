from django import forms

from debts.models import DebtRepayment

class DebtRepaymentForm(forms.ModelForm):

    class Meta:
        model = DebtRepayment
        fields = [
            "paid_at",
            "amount",
            "repaid_by",
            "note"
        ]
     


