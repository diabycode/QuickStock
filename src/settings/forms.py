from django import forms

from settings.models import EditableSettings

class SettingsModelfForm(forms.ModelForm):
    password_confirm = forms.CharField(max_length=130, label="Mot de passe", required=True,
                                       widget=forms.PasswordInput(attrs={
                                           "placeholder": "Saisissez votre mot de passe pour confirmer"
                                       }))

    class Meta:
        model = EditableSettings
        fields = ["company_name", "company_logo"]
        widgets = {
            "company_logo": forms.ClearableFileInput()
        }
        

