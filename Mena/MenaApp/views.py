from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Post
from .models import Symptoms
from .forms import SymptomsForm

# Create your views here.
@login_required(login_url='/login/')
def home(request):
    return render(request, "auth/home.html")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/MenaApp/home")
    else:
        form = RegisterForm()
    return render(request, "auth/register.html", {"form":form})

@login_required(login_url='/login/')
def post_forum(request):
    posts = Post.objects.all()
    return render(request, "forum/forum.html", {"posts": posts})

def logout_view(request):
    logout(request)
    return redirect('/')

class SymptomsView(View):
    def get(self, request):
        symptoms = Symptoms.objects.all()  # Get all symptoms
        form = SymptomsForm()  # Create an empty form
        context = {
            'symptoms': symptoms,
            'form': form,
        }
        return render(request, 'symptoms.html', context)

    def post(self, request):
        form = SymptomsForm(request.POST)  # Get data from the form
        if form.is_valid():
            form.save()  # Save the new symptom
            return redirect('phase_symptoms')  # Redirect to the same page
        else:
            symptoms = Symptoms.objects.all()  # Get existing symptoms again if form is invalid
            context = {
                'symptoms': symptoms,
                'form': form,
            }
            return render(request, 'symptoms.html', context)
    
