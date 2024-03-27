from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic import View
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserLoginForm, UserRegistrationForm
from .models import UserModel


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
    success_redirect_url = reverse_lazy('home') 

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(self.success_redirect_url)

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
                return render(request, self.template_name, {'form': form, 'error': 'User does not exist'})
            else:

                # verif password
                if user.check_password(password):
                    
                    # login user
                    from django.contrib.auth import login
                    login(request, user)
                    return redirect(self.success_redirect_url)
                
                return render(request, self.template_name, {'form': form, 'error': 'Password is incorrect'}) 
        
        return render(request, self.template_name, {'form': form})
    

class CustomRegistrationView(View):

    registration_form = UserRegistrationForm
    template_name = 'accounts/registration.html'
    success_redirect_url = reverse_lazy('home')


    def get(self, request):
        if request.user.is_authenticated:
            return redirect(self.success_redirect_url)

        form = self.registration_form()
        context = {
            'form': form
        }

        return render(request, 'accounts/registration.html', context)

    def post(self, request):
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

