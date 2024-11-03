from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import logout

# Create your views here.
def home(request):
    return render(request, "auth/home.html")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("/Mena_register/home")
    else:
        form = RegisterForm()
    return render(request, "auth/register.html", {"form":form})

def forums(request):
    pass

def logout_view(request):
    logout(request)
    return redirect('/')
