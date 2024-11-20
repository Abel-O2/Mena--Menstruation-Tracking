from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, PeriodForm
from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Post
from .models import Period, Mood
from datetime import date
from .models import Symptoms
from .models import Calendar
from .forms import SymptomsForm, PostsForm, CalendarForm
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
def get_forum(request):
    posts = Post.objects.all()
    return render(request, "forum/forum.html", {"posts": posts})

def post_forum(request):
    if request.method == "POST":
        form = PostsForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.userID = request.user
            post.save()
            return redirect('/MenaApp/forum')
    else:
        form = PostsForm()
    return render(request, "forum/post.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def period_tracker(request):
    # Example data; replace with actual period data for logged-in user
    user_period = Period.objects.filter(user=request.user).first()
    user_mood = Mood.objects.filter(user=request.user, date=date.today()).first()

    context = {
        'user': request.user,
        'period': user_period,
        'mood': user_mood,
        'today': date.today(),
    }
    return render(request, 'womendashboard/period_tracker.html', context)

def edit_period(request, period_id):
    period = get_object_or_404(Period, id=period_id)
    
    if request.method == 'POST':
        form = PeriodForm(request.POST, instance=period)
        if form.is_valid():
            form.save()
            return redirect('period_tracker')  # Redirect to period tracker page or another page after saving
    else:
        form = PeriodForm(instance=period)

    context = {
        'form': form,
        'period': period
    }
    return render(request, 'womendashboard/edit_period.html', context)
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
        events = [
            {
                'id': event.id,
                'title': event.title,
                'start': event.start_time.isoformat(),
                'end': event.end_time.isoformat(),
                'is_pinned': event.is_pinned
            } for event in period
        ]
        return JsonResponse(events, safe=False)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title', 'Untitled Event')
            start_time = data.get('start')
            end_time = data.get('end')
            is_pinned = data.get('is_pinned', False)

            if not start_time or not end_time:
                return JsonResponse({"error": "Start time and end time are required."}, status=400)
            
            # Creating a new event
            event = Calendar.objects.create(
                title=title,
                start_time=start_time,
                end_time=end_time,
                is_pinned=is_pinned
            )
            return JsonResponse({"id": event.id}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)

    elif request.method == 'PATCH':
        try:
            data = json.loads(request.body)
            period_id = data.get('id')
            if not period_id or 'is_pinned' not in data:
                return JsonResponse({"error": "Missing 'id' or 'is_pinned' parameter"}, status=400)
            
            # Updating an existing event
            Calendar.objects.filter(id=period_id).update(is_pinned=data['is_pinned'])
            return JsonResponse({"status": "success"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)

    else:
        return JsonResponse({"error": "Method not allowed."}, status=405)


'''
def calendar_view(request):
    return render(request, 'calendar.html')

@csrf_exempt
def timeOfTheMonth(request):
    if request.method == 'GET':
        period = Calendar.objects.all()
        return render(request, 'calendar.html', {'period': period})
    elif request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title', 'Untitled Event')
        start_time = data.get('start')
        end_time = data.get('end')
        is_pinned = data.get('is_pinned', False)
        
        if not start_time or not end_time:
            return JsonResponse({"error": "Start time and end time are required."}, status=400)
        
        # Creating a new event
        event = Calendar.objects.create(
            title=title,
            start_time=start_time,
            end_time=end_time,
            is_pinned=is_pinned
        )
        return JsonResponse({"id": event.id}, status=201)
    
    elif request.method == 'PATCH':
        data = json.loads(request.body)
        period_id = data.get('id')
        if not period_id or 'is_pinned' not in data:
            return JsonResponse({"error": "Missing 'id' or 'is_pinned' parameter"}, status=400)
        
        # Updating an existing event
        Calendar.objects.filter(id=period_id).update(is_pinned=data['is_pinned'])
        return JsonResponse({"status": "success"})
'''


'''
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
    elif request.method == 'POST':
        data = json.loads(request.body)
        period_id = data.get('id')
        if period_id is None or 'is_pinned' not in data:
            return JsonResponse({"error": "Missing 'id' or 'is_pinned' parameter"}, status=400)
        Calendar.objects.filter(id=period_id).update(is_pinned=data['is_pinned'])
        return JsonResponse({"status": "success"})'''
