from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render


@login_required(login_url='/accounts/login/')
def home(request):
    context = {}
    context["page_title"] = "Tableau de bord"
    return render(request, "quickstockapp/dashboard.html", context=context)



