import random
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, PeriodForm
from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Post, Comment
from .models import Period, Mood
from datetime import date
from .models import Symptoms
from .models import Calendar
from .forms import SymptomsForm, PostsForm, CalendarPinForm, PinForm, CommentForm, UserUpdateForm
import json
from django.views.decorators.csrf import csrf_exempt
from django import forms
from MenaApp.models import CyclePhase, Lesson
import calendar
from datetime import date, timedelta
from urllib.parse import unquote

# Create your views here.
@login_required(login_url='/login/')
def home(request):
    return render(request, "womendashboard/period_tracker.html")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/MenaApp/home")
    else:
        form = RegisterForm()
    return render(request, "auth/register.html", {"form":form})

@login_required
def profile_view(request):
    user = request.user
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'profile.html', {'form': form})

@login_required
def delete_account(request):
    user = request.user
    if request.method == "POST":
        user.delete()
        logout(request)
        return redirect('login')
    return redirect('login')

# Post CRUD
@login_required(login_url='/login/')
def get_forum(request):
    posts = Post.objects.all()
    return render(request, "forum/forum.html", {"posts": posts})

@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
def delete_forum(request, id):
    post = Post.objects.get(id=id)
    if post.userID == request.user:
        post.delete()
    return redirect('forum')

@login_required(login_url='/login/')
def edit_forum(request, id):
    post = Post.objects.get(id=id)

    if post.userID == request.user:
        if request.method == "POST":
            form = PostsForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return redirect('forum')
        else:
            form = PostsForm(instance=post)

    return render(request, "forum/edit_post.html", {"form": form})

# Comment CRUD
@login_required
def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.userID = request.user
            comment.postID = post
            comment.save()
            return redirect('forum')  # Redirect to your forum page or the post's detail page
    else:
        form = CommentForm()
    return render(request, 'comment/add_comment.html', {'form': form, 'post': post})

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, userID=request.user)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('forum')
    else:
        form = CommentForm(instance=comment)
    return render(request, 'comment/edit_comment.html', {'form': form})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, userID=request.user)
    if comment.userID == request.user:
        comment.delete()
    return redirect('forum')

def logout_view(request):
    logout(request)
    return redirect('/')


# Temporary form for simulation
class SimulatedDayForm(forms.Form):
    simulated_day = forms.IntegerField(
        label="Simulated Day",
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter day (e.g., 1, 2, 3)', 'style': 'width: 100%; padding: 5px; margin-top: 5px; border-radius: 4px;'})
    )



@login_required
def period_tracker(request):
    user_period = Period.objects.filter(user=request.user).first()
    simulated_day = None
    current_phase = None
    lessons = []

    today = date.today()
    year, month = today.year, today.month
    cal = calendar.Calendar()
    month_days = list(cal.itermonthdays(year, month))
    pinned_days = Calendar.objects.filter(year=year, month=month).values_list('day', flat=True)

    if request.method == 'POST':
        form = SimulatedDayForm(request.POST)
        if form.is_valid():
            simulated_day = form.cleaned_data.get('simulated_day')
    else:
        form = SimulatedDayForm()

    actual_day = (date.today() - user_period.start_date).days % user_period.cycle_length if user_period else 1
    current_day = simulated_day or actual_day

    current_phase = CyclePhase.objects.filter(start_day__lte=current_day, end_day__gte=current_day).first()

    if current_phase:
        symptoms_list = [symptom.strip() for symptom in current_phase.symptoms.split(',')]
        moods = current_phase.mood.split(",")
        random_mood = random.choice(moods).strip()
        lessons = Lesson.objects.filter(phase=current_phase.name.lower())
    else:
        symptoms_list = ["No symptoms available."]
        mood = "No mood information available."
    
    context = {
        'user': request.user,
        'period': user_period,
        'today': date.today(),
        'simulated_day': simulated_day,
        'actual_day': actual_day,
        'current_phase': current_phase,
        'symptoms_list': symptoms_list,
        'mood': random_mood,
        'lessons': lessons,
        'form': form,
         'year': year,
        'month': month,
        'month_name': calendar.month_name[month],
        'days': month_days,
        'pinned_days': pinned_days,
        'previous_year': year - 1,
        'next_year': year + 1,
        'previous_month': month - 1 if month > 1 else 12,
        'next_month': month + 1 if month < 12 else 1,
    }
    return render(request, 'womendashboard/period_tracker.html', context)


@login_required
def edit_period(request, period_id):
    period = get_object_or_404(Period, id=period_id)
    
    if request.method == 'POST':
        form = PeriodForm(request.POST, instance=period)
        if form.is_valid():
            form.save()
            return redirect('period_tracker')
    else:
        form = PeriodForm(instance=period)

    context = {
        'form': form,
        'period': period
    }
    return render(request, 'womendashboard/edit_period.html', context)


@login_required
def calendar_view(request, year=None, month=None):
    if year is None or month is None:
        today = date.today()
        year = int(year) if year else today.year
        month = int(month) if month else today.month

    #Dyas of the month
    cal = calendar.Calendar()
    month_days = list(cal.itermonthdays(year, month))
    
    #Get code for the days in the current month
    pinned_days = Calendar.objects.filter(year=year, month=month).values_list('day', flat=True)

    #For the create and delete functions
    if request.method == 'POST':
        form = PinForm(request.POST)
        if form.is_valid():
            day = form.cleaned_data['day']
            if 'delete' in request.POST:
                Calendar.objects.filter(year=year, month=month, day=day).delete()
            else:
                for i in range(5):
                    pin_date = date(year, month, day) + timedelta(days=i)
                    Calendar.objects.update_or_create(
                        year=pin_date.year,
                        month=pin_date.month,
                        day=pin_date.day,
                        defaults={'is_pinned': True, 'pinned_date': pin_date}
                    )
        return redirect('calendar_view', year=year, month=month)

    else:
        form = PinForm()

    request.session['pinned_days'] = list(pinned_days)

    pinned_events = Calendar.objects.filter(year=year, month=month)
    expired_days = [event.day for event in pinned_events if event.is_expired()]

    previous_month = month - 1 if month > 1 else 12
    next_month = month + 1 if month < 12 else 1
    previous_year = year if month > 1 else year - 1
    next_year = year if month < 12 else year + 1

    context = {
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month],
        'days': month_days,
        'pinned_days': pinned_days,
        'expired_days': expired_days,
        'form': form,
        'previous_month': previous_month,
        'previous_year': previous_year,
        'next_month':  next_month,
        'next_year':  next_year,
        'current_year': year,
        'current_month': month
    }
    return render(request, 'calendar.html', context)