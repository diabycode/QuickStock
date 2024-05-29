from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic import UpdateView
from django.views.generic import View
from django.contrib.auth import login
from django.http import HttpRequest
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.forms import UserLoginForm, UserRegistrationForm, UserPinCodeForm
from accounts.models import UserModel, UserPreference


class CustomLogoutView(View):
    login_url = reverse_lazy('accounts:login')

    def get(self, request):
        if request.user.is_authenticated:
            from django.contrib.auth import logout
            logout(request)
        return redirect(self.login_url)


class CustomLoginView(View):

    authentication_form = UserLoginForm
    template_name = 'accounts/login.html'
    success_redirect_url = reverse_lazy('products:product_list') 

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(self.success_redirect_url)

        if not UserModel.objects.first():
            return redirect("accounts:register")
        form = self.authentication_form()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        
        form = self.authentication_form(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data.get('username')
            password = data.get('password')

            try:
                user = UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                return render(request, self.template_name, {'form': form, 'error': 'Nom d\'utilisateur ou mot de passe incorrete'})
            else:

                # verif password
                if user.check_password(password):
                    
                    # login user
                    from django.contrib.auth import login
                    login(request, user)

                    redirect_url = request.GET.get("next", self.success_redirect_url) 
                    return redirect(redirect_url)
                
                return render(request, self.template_name, {'form': form, 'error': 'Nom d\'utilisateur ou mot de passe incorrete'}) 
        
        return render(request, self.template_name, {'form': form})
    

class CustomRegistrationView(View):

    registration_form = UserRegistrationForm
    template_name = 'accounts/registration.html'
    success_redirect_url = reverse_lazy('home')


    def get(self, request):
        if request.user.is_authenticated:
            return redirect(self.success_redirect_url)

        if UserModel.objects.first():
            return redirect("accounts:login")

        form = self.registration_form()
        context = {
            'form': form
        }

        return render(request, 'accounts/registration.html', context)

    def post(self, request):
        if UserModel.objects.first():
            return redirect("accounts:login")

        form = self.registration_form(request.POST)
        if form.is_valid():
            user = form.save()
            if user:
                user.set_password(user.password)
                user.save()

                from django.contrib.auth import login
                login(request, user)
                return redirect(self.success_redirect_url)
        
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class AccountDetailsView(LoginRequiredMixin, View):

    def get(self, request: HttpRequest):
        context = self.get_context_data(request)
        return render(request, "accounts/details.html", context)
    
    def post(self, request: HttpRequest):
        if request.POST.get("request") == "change_pin_code":
            form = UserPinCodeForm(request.POST)
            if form.is_valid():
                password_confirm: str = form.cleaned_data.get("password_confirm")
                if request.user.check_password(password_confirm):
                    form_data = form.cleaned_data
                    user_preferance = UserPreference.objects.get(user=request.user)
                    user_preferance.pin_code = form_data.get("pin_code")
                    user_preferance.save()
                    messages.success(request, "Code pin modifié avec succès", extra_tags="message")
                    return redirect(reverse("accounts:details"))
                messages.error(request, "Mot de passe incorrect", extra_tags="message")
                return redirect(reverse("accounts:details"))
            context = self.get_context_data(request)
            context["pin_code_form"] = form
            messages.error(request, "Echec : Erreur dans la saisie", extra_tags="message")
            return render(request, "accounts/details.html", context)
        
        elif request.POST.get("request") == "change_password":
            data = request.POST
            user = request.user

            current_password: str = data.get("current_password")
            if not user.check_password(current_password):
                context = self.get_context_data(request)
                context["password_change_faild"] = "Mot de passe actuel incorrect"
                return render(request, "accounts/details.html", context)
            
            new_password: str = data.get("new_password")
            new_password_repeat = data.get("new_password_repeat")
            if not new_password == new_password_repeat:
                context = self.get_context_data(request)
                context["password_change_faild"] = "Nouveaux mot de passe différents"
                return render(request, "accounts/details.html", context)

            user.set_password(new_password)
            user.save()  
            login(request=request, user=user)
            return redirect("accounts:password_changed")
        
        context = self.get_context_data(request=request)
        return render(request, "accounts/details.html", context)

    def get_context_data(self, request: HttpRequest) -> dict:
        context = {
            "user": request.user,
            "pin_code_form": UserPinCodeForm,
        }
        return context


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = UserModel
    fields = [
        "username",
        "email",
        "first_name",
        "last_name",
    ]
    template_name = "accounts/update.html"
    success_url = reverse_lazy("accounts:details")

    def get_object(self, queryset=None):
        return self.request.user


@login_required(login_url="/accounts/login/")
def password_changed(request):
    return render(request, "accounts/password_changed.html")