from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Post
from .models import Symptoms
from .models import Calendar
from .forms import SymptomsForm
import json
from django.views.decorators.csrf import csrf_exempt

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

def calendar_view(request):
    return render(request, 'calendar.html')

@csrf_exempt 
def timeOfTheMonth(request):
    if request.method == 'GET':
        period = Calendar.objects.all()
        return render(request,'calendar.html',{'period':period})
    elif request.method == 'POST':
        data = json.loads(request.body)
        mark = Calendar.objects.create(
            title=data['title', 'Untitled Event'],
            start_time=data['start',None],
            end_time=data['end',None],
            is_pinned=data.get('is_pinned', False)
        )
        return JsonResponse({"id": mark.id}, status=201)
    elif request.method == 'PATCH':
        data = json.loads(request.body)
        period_id = data.get('id')
        if period_id is None or 'is_pinned' not in data:
            return JsonResponse({"error": "Missing 'id' or 'is_pinned' parameter"}, status=400)
        Calendar.objects.filter(id=period_id).update(is_pinned=data['is_pinned'])
        return JsonResponse({"status": "success"})
    
