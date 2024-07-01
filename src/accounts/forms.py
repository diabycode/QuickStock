import re

from django import forms

from .models import UserModel, UserPreference

class UserLoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Nom d\'utilisateur'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Mot de passe'})


class UserRegistrationForm(forms.ModelForm):
        
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Nom d\'utilisateur'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email (optionel)'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Mot de passe'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Prénom'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Nom'})

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        widgets = {
            'password': forms.PasswordInput
        }

    def clean_username(self):
        excluded = ["$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", "{", "}", "[", "]", ":", ";", "'", '"', "<", ">", ",", ".", "?", "/", "|", "~", "`"]
        username = self.cleaned_data['username']
        username.strip()

        for c in username:
            if c in excluded:
                raise forms.ValidationError("Le nom d'utilisateur ne peut pas contenir de caractères spéciaux")

        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        password.strip()

        if len(password) < 8:
            raise forms.ValidationError("Le mot de passe doit comporter au moins 8 caractères")

        # include numbers
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("Le mot de passe doit contenir au moins un chiffre")
        
        # include uppercase
        if not any(char.isupper() for char in password):
            raise forms.ValidationError("Le mot de passe doit contenir au moins une lettre majuscule")
        
        # include lowercase
        if not any(char.islower() for char in password):
            raise forms.ValidationError("Le mot de passe doit contenir au moins une lettre minuscule")
    
        # include special characters
        special_characters = ["@", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", "{", "}", "[", "]", ":", ";", "'", '"', "<", ">", ",", ".", "?", "/", "|", "~", "`"]
        if not any(char in special_characters for char in password):
            raise forms.ValidationError("Le mot de passe doit contenir au moins un caractère spécial")
        
        return password

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        last_name.strip()

        r = re.compile(r'^[a-zA-Z]+$')
        if not r.match(last_name):
            raise forms.ValidationError("Le nom de famille ne doit contenir que des lettres")

        return last_name
    
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        first_name.strip()

        # alpha only regex and space
        r = re.compile(r'^[a-zA-Z ]+$')

        if not r.match(first_name):
            raise forms.ValidationError("Le prénom ne doit contenir que des lettres")

        return first_name


class UserPinCodeForm(forms.ModelForm):
    password_confirm = forms.CharField(max_length=130, label="Mot de passe", required=True,
                                       widget=forms.PasswordInput(attrs={
                                           "placeholder": "Saisissez votre mot de passe pour confirmer"
                                       }))

    class Meta:
        model = UserPreference
        fields = ["pin_code"]
        widgets = {
            "pin_code": forms.PasswordInput(
                attrs={
                    "placeholder": "Nouveau code pin"
                }
            )
        }


class UserCreateForm(UserRegistrationForm):

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UserModel
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "is_superuser",
            "is_active",
            "groups",      
            "user_permissions",
        ]
        exclude = ['password']


class UserPasswordChangeForm(UserRegistrationForm):

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UserModel
        fields = ["password"]
        widgets = {
            "password": forms.PasswordInput(
                attrs={
                    "placeholder": "Entrez un mot de passe sécurisé"
                }
            )
        }

    def clean_password(self):
        return self.cleaned_data['password']