import re

from django import forms

from .models import UserModel


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
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
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
                raise forms.ValidationError("Username cannot contain special characters")

        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        password.strip()

        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long")

        # include numbers
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("Password must contain at least one number")
        
        # include uppercase
        if not any(char.isupper() for char in password):
            raise forms.ValidationError("Password must contain at least one uppercase letter")
        
        # include lowercase
        if not any(char.islower() for char in password):
            raise forms.ValidationError("Password must contain at least one lowercase letter")
    
        # include special characters
        special_characters = ["@", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", "{", "}", "[", "]", ":", ";", "'", '"', "<", ">", ",", ".", "?", "/", "|", "~", "`"]
        if not any(char in special_characters for char in password):
            raise forms.ValidationError("Password must contain at least one special character")
        
        return password

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        last_name.strip()

        r = re.compile(r'^[a-zA-Z]+$')
        if not r.match(last_name):
            raise forms.ValidationError("Last name must only contain letters")

        return last_name
    
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        first_name.strip()

        # alpha only regex and space
        r = re.compile(r'^[a-zA-Z ]+$')

        if not r.match(first_name):
            raise forms.ValidationError("Fisrt name must only contain letters")

        return first_name




