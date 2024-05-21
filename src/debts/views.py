from typing import Any
from django.forms import BaseModelForm
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required

from debts.models import Debt
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
            Debt.order.field.verbose_name,
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
        context["repayment_list"] = debt.debtrepayment_set.all().order_by("-paid_at")
        return context


class DebtCreateView(LoginRequiredMixin, CreateView):
    model = Debt
    template_name = "debts/debt_create.html"
    success_url = reverse_lazy("debts:debt_list")
    fields = [
        "granted_date",
        "granted_by",
        "initial_amount",
        "order",
    ]
    def get_form(self, form_class: type[BaseModelForm] | None = None) -> BaseModelForm:
        form = super().get_form(form_class)
        store_pk = self.request.session.get("current_store_pk")
        store = None
        if store_pk:
            store = get_object_or_404(Store, pk=store_pk)
        form.fields["order"].queryset = Order.objects.filter(store=store).order_by("-add_at")
        return form 


class DebtUpdateView(LoginRequiredMixin, UpdateView):
    model = Debt
    template_name = "debts/debt_update.html"
    fields = [
        "granted_date",
        "granted_by",
        "initial_amount",
        "order",
    ]

    def get_success_url(self) -> str:
        obj = self.get_object()
        return reverse("debts:debt_details", kwargs={"pk": obj.pk})

    def get_form(self, form_class: type[BaseModelForm] | None = None) -> BaseModelForm:
        form = super().get_form(form_class)
        store_pk = self.request.session.get("current_store_pk")
        store = None
        if store_pk:
            store = get_object_or_404(Store, pk=store_pk)
        form.fields["order"].queryset = Order.objects.filter(store=store).order_by("-add_at")
        return form 


class DebtDeleteView(LoginRequiredMixin, DeleteView):
    model = Debt
    template_name = "debts/debt_delete.html"
    success_url = reverse_lazy("debts:debt_list")


@login_required(login_url='/accounts/login/')
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
