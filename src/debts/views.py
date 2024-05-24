from typing import Any
import datetime
import pytz

from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required

from debts.models import Debt, DebtRepayment
from debts.forms import DebtRepaymentForm
from orders.models import Order
from stores.models import Store


class DebtListView(LoginRequiredMixin, ListView):
    model = Debt
    template_name = "debts/debt_list.html"
    context_object_name = "debt_list"
    queryset = Debt.objects.all().order_by("-add_at")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        debt_column_names = [
            Debt.granted_date.field.verbose_name,
            Debt.granted_by.field.verbose_name,
            Debt.initial_amount.field.verbose_name,
            "Reste à payer",
            Debt.store.field.verbose_name,
        ]
        
        context["debt_column_names"] = debt_column_names
        return context


class DebtDetailView(LoginRequiredMixin, DetailView):
    model = Debt
    template_name = "debts/debt_details.html"
    context_object_name = "debt"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        debt = self.get_object()
        context["repayment_list"] = debt.debtrepayment_set.all().order_by("-add_at")
        return context


class DebtCreateView(LoginRequiredMixin, CreateView):
    model = Debt
    template_name = "debts/debt_create.html"
    success_url = reverse_lazy("debts:debt_list")
    fields = [
        "granted_date",
        "granted_by",
        "initial_amount",
        "store",
    ]

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        granted_date: datetime.date = form.cleaned_data.get("granted_date")
        now_date = datetime.datetime.now().date()

        if granted_date > now_date:
            form.add_error("granted_date", "Erreur de date")
            return self.form_invalid(form=form)
        
        return super().form_valid(form)


class DebtUpdateView(LoginRequiredMixin, UpdateView):
    model = Debt
    template_name = "debts/debt_update.html"
    fields = [
        "granted_date",
        "granted_by",
        "initial_amount",
        "store",
    ]

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        granted_date: datetime.date = form.cleaned_data.get("granted_date")
        now_date = datetime.datetime.now().date()

        if granted_date > now_date:
            form.add_error("granted_date", "Erreur de date")
            return self.form_invalid(form=form)
        
        return super().form_valid(form)

    def get_success_url(self) -> str:
        obj = self.get_object()
        return reverse("debts:debt_details", kwargs={"pk": obj.pk})


class DebtDeleteView(LoginRequiredMixin, DeleteView):
    model = Debt
    template_name = "debts/debt_delete.html"
    success_url = reverse_lazy("debts:debt_list")


@login_required(login_url="/accounts/login/")
def debt_repayment(request: HttpRequest, debt_pk):
    context = {}
    debt = get_object_or_404(Debt, pk=debt_pk)
    context["debt"] = debt

    form = DebtRepaymentForm()
    context["form"] = form

    if request.method == "POST":
        # get data save if great and redirect to debt details
        form = DebtRepaymentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            if instance.amount > debt.remaining_amount:
                form.add_error("amount", f"Erreur dans le montant; Le reste à payer {debt.remaining_amount} FCFA")
                context["form"] = form
                return render(request, "debts/debt_repayment.html", context)
            instance.debt = debt
            instance.save()
            return redirect(
                reverse("debts:debt_details", kwargs={"pk": debt.pk})
            )
        context["form"] = form
        return render(request, "debts/debt_repayment.html", context)

    return render(request, "debts/debt_repayment.html", context)


@login_required(login_url="/accounts/login/")
def edit_repayment(request: HttpRequest, debt_pk, repayment_pk):
    context = {}
    debt = get_object_or_404(Debt, pk=debt_pk)
    repayment = get_object_or_404(DebtRepayment, pk=repayment_pk)
    context["repayment"] = repayment
    context["debt"] = debt

    form = DebtRepaymentForm(instance=repayment)
    context["form"] = form

    if request.method == "POST":
        # get data save if great and redirect to debt details
        form = DebtRepaymentForm(request.POST, instance=repayment)
        if form.is_valid():
            instance = form.save(commit=False)
            if instance.amount > debt.remaining_amount:
                form.add_error("amount", f"Erreur dans le montant; Le reste à payer {debt.remaining_amount} FCFA")
                context["form"] = form
                return render(request, "debts/edit_repayment.html", context)
            instance.debt = debt
            instance.save()
            return redirect(
                reverse("debts:debt_details", kwargs={"pk": debt.pk})
            )
        context["form"] = form
        return render(request, "debts/edit_repayment.html", context)

    return render(request, "debts/edit_repayment.html", context)


@login_required(login_url="/accounts/login/")
def repayment_delete(request: HttpRequest, debt_pk, repayment_pk):
    if request.method == "POST":
        repayment = get_object_or_404(DebtRepayment, pk=repayment_pk)
        repayment.delete()
        return redirect(reverse("debts:debt_details", kwargs={"pk": debt_pk}))
    
    return render(request, "debts/repayment_delete.html")


