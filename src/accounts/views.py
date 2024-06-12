from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.views.generic import UpdateView, ListView, DetailView, CreateView, DeleteView
from django.views.generic import View
from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.admin.models import LogEntry
from django.contrib import messages
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import ADDITION, DELETION, CHANGE

from accounts.forms import UserLoginForm, UserRegistrationForm, UserPinCodeForm, UserCreateForm, UserPasswordChangeForm
from accounts.models import UserModel, UserPreference
from accounts.utils import log_user_action
from accounts.mixins import MyPermissionRequiredMixin
from accounts.decorators import permission_required
from accounts.utils import get_all_permissions
from accounts.widgets import PermissionSelectWidget


class CustomLogoutView(View):
    login_url = reverse_lazy('accounts:login')

    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            from django.contrib.auth import logout
            log_user_action(
                user=request.user,
                obj=request.user,
                action_flag=CHANGE,
                change_message="Déconnexion"
            )
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
                    log_user_action(
                        user=user,
                        obj=user,
                        action_flag=CHANGE,
                        change_message="Connexion au système"
                    )
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


# users views

class UserListView(LoginRequiredMixin, MyPermissionRequiredMixin, ListView):
    model = UserModel
    template_name = "accounts/user_list.html"
    permission_required = "accounts.can_view_user"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = UserModel.objects.all().order_by("-join_date").exclude(
            username=self.request.user.username)
        context["user_list"] = queryset

        account_column_names = [
            UserModel.username.field.verbose_name,
            UserModel.last_name.field.verbose_name,
            UserModel.first_name.field.verbose_name,
            UserModel.join_date.field.verbose_name,
            "Mot de passe"
        ]
        context["user_column_names"] = account_column_names
        context["page_title"] = "Gestion des utilisateurs"
        return context


class UserCreateView(LoginRequiredMixin, MyPermissionRequiredMixin, CreateView):
    model = UserModel
    template_name = "accounts/user_create.html"
    form_class = UserCreateForm
    success_url = reverse_lazy("accounts:user_list")
    permission_required = "accounts.can_add_user"

    def get_form(self, form_class: type[BaseModelForm] | None=None) -> BaseModelForm:
        form = super().get_form(form_class)
        permissions = get_all_permissions(edit_default=True, excludes=[
            "userpreference",
            "contenttype",
            "permission",
            "logentry",
            "session",
            "editablesettings",
        ] )
        form.fields["user_permissions"].widget = PermissionSelectWidget()
        form.fields["user_permissions"].queryset = permissions
        return form

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form_valid_response = super().form_valid(form)
        new_user: UserModel = form.instance
        # new_user.set_password(form.cleaned_data.get("password"))
        # new_user.save()
        log_user_action(
            user=self.request.user,
            obj=new_user,
            action_flag=ADDITION,
            change_message="Utilisateur ajouté"
        )
        return form_valid_response


class UserUpdateView(LoginRequiredMixin, MyPermissionRequiredMixin, UpdateView):
    model = UserModel
    form_class = UserCreateForm
    template_name = "accounts/user_update.html"
    extra_context = {
        "page_title": "Gestion des utilisateurs",
    }
    context_object_name = "user_object"
    permission_required = "accounts.can_change_user"

    def get_success_url(self) -> str:
        return reverse("accounts:user_list")
    
    def get_form(self, form_class: type[BaseModelForm] | None=None) -> BaseModelForm:
        form = super().get_form(form_class)
        permissions = get_all_permissions(edit_default=True, excludes=[
            "userpreference",
            "contenttype",
            "permission",
            "logentry",
            "session",
            "editablesettings",
        ])
        form.fields["user_permissions"].widget = PermissionSelectWidget()
        form.fields["user_permissions"].queryset = permissions
        return form

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form_valid = super().form_valid(form)
        user: UserModel = form.instance
        # user.set_password(form.cleaned_data.get("password"))
        # user.save()
        log_user_action(
            user=self.request.user,
            obj=user,
            action_flag=CHANGE,
            change_message="Utilisateur modifié"
        )
        return form_valid


class UserDetailsView(LoginRequiredMixin, MyPermissionRequiredMixin, DetailView):
    model = UserModel
    context_object_name = "user_object"
    template_name = "accounts/user_details.html"
    permission_required = "accounts.can_view_user"


class UserDeleteView(LoginRequiredMixin, MyPermissionRequiredMixin, DeleteView):
    model = UserModel
    template_name = "accounts/user_delete.html"
    context_object_name = "user_object"
    success_url = reverse_lazy("accounts:user_list")
    permission_required = "accounts.can_delete_user"

    def form_valid(self, form):
        log_user_action(
            user=self.request.user,
            obj=self.get_object(),
            action_flag=DELETION,
            change_message="Utlisateur supprimé"
        )
        return super(DeleteView, self).form_valid(form)


@login_required(login_url="/accounts/login/")
def password_changed(request):
    return render(request, "accounts/password_changed.html")


@login_required(login_url="/accounts/login/")
@permission_required("accounts.can_change_user")
def change_user_password(request: HttpRequest, pk):
    context = {}
    user = get_object_or_404(UserModel, pk=pk)
    form = UserPasswordChangeForm()

    if request.method == "POST":
        form = UserPasswordChangeForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data.get("password"))
            user.save()
            messages.success(request, "Mot de passe mise à jour", extra_tags="message")
            return redirect(reverse("accounts:user_list"))
    context["user"] = user
    context["form"] = form
    return render(request, "accounts/change_user_password.html", context)


class GroupListView(LoginRequiredMixin, MyPermissionRequiredMixin, ListView):
    model = Group
    template_name = "accounts/group_list.html"
    context_object_name = "group_list"
    extra_context = {"page_title": "Groupes & Accès"}
    permission_required = "auth.view_group"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group_column_names = [
            Group.name.field.verbose_name,
        ]
        context["group_column_names"] = group_column_names
        return context


class GroupCreateView(LoginRequiredMixin, MyPermissionRequiredMixin, CreateView):
    model = Group
    fields= [
        "name",
        "permissions",
        "description"
    ]
    template_name = "accounts/group_create.html"
    success_url = reverse_lazy("accounts:group_list")
    extra_context = {"page_title": "Groupes & Accès"}
    permission_required = "auth.add_group"

    def get_form(self, form_class: type[BaseModelForm] | None=None) -> BaseModelForm:
        form = super().get_form(form_class)
        permissions = get_all_permissions(edit_default=True, excludes=[
            "userpreference",
            "contenttype",
            "permission",
            "logentry",
            "session",
            "editablesettings",
        ])
        form.fields["permissions"].widget = PermissionSelectWidget()
        form.fields["permissions"].queryset = permissions
        return form

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form_valid_response = super().form_valid(form)
        log_user_action(
            user=self.request.user,
            obj=form.instance,
            action_flag=ADDITION,
            change_message="Groupe ajouté"
        )
        return form_valid_response


class GroupUpdateView(LoginRequiredMixin, MyPermissionRequiredMixin, UpdateView):
    model = Group
    fields= [
        "name",
        "permissions",
        "description"
    ]
    template_name = "accounts/group_update.html"
    success_url = reverse_lazy("accounts:group_list")
    extra_context = {"page_title": "Groupes & Accès"}
    context_object_name = "group"
    permission_required = "auth.change_group"

    def get_form(self, form_class: type[BaseModelForm] | None=None) -> BaseModelForm:
        form = super().get_form(form_class)
        permissions = get_all_permissions(edit_default=True, excludes=[
            "userpreference",
            "contenttype",
            "permission",
            "logentry",
            "session",
            "editablesettings",
        ])
        form.fields["permissions"].widget = PermissionSelectWidget()
        form.fields["permissions"].queryset = permissions
        return form

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form_valid_response = super().form_valid(form)
        log_user_action(
            user=self.request.user,
            obj=self.get_object(),
            action_flag=CHANGE,
            change_message="Groupe modifié"
        )
        return form_valid_response


class GroupDeleteView(LoginRequiredMixin, MyPermissionRequiredMixin, DeleteView):
    model = Group
    template_name = "accounts/group_delete.html"
    context_object_name = "group"
    success_url = reverse_lazy("accounts:group_list")
    permission_required = "auth.delete_group"

    def form_valid(self, form):
        log_user_action(
            user=self.request.user,
            obj=self.get_object(),
            action_flag=DELETION,
            change_message="Groupe supprimé"
        )
        return super(DeleteView, self).form_valid(form)


class UserActionLogList(LoginRequiredMixin, MyPermissionRequiredMixin, ListView):
    model = LogEntry
    template_name = "accounts/user_action_logs.html"
    context_object_name = "user_action_logs"
    queryset = LogEntry.objects.all().order_by("-action_time")
    permission_required = "admin.view_logentry"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        log_column_names = [
            "Date & Heure",
            "Auteur",
            "Type de contenu",
            "Contenu",
            "Action",
        ]
        context["log_column_names"] = log_column_names
        return context 
