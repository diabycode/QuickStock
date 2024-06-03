import datetime
import pytz

from django import forms

from debts.models import DebtRepayment, Debt


class DebtRepaymentForm(forms.ModelForm):

    class Meta:
        model = DebtRepayment
        fields = [
            "paid_at",
            "amount",
            "repaid_by",
            "note"
        ]
    
    def clean_paid_at(self):
        utc = pytz.UTC
        paid_at: datetime.datetime  =  self.cleaned_data["paid_at"]
        now = utc.localize(datetime.datetime.now())
        if paid_at > now:
            raise forms.ValidationError("Erreur dans la date") 
        return paid_at
     

class DebtTypeForm(forms.ModelForm):
    
    class Meta:
        model = Debt
        fields = ["debt_type"]

