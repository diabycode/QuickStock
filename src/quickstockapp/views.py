from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render


@login_required(login_url='/accounts/login/')
def home(request):
    return render(request, "quickstockapp/dashboard.html")



