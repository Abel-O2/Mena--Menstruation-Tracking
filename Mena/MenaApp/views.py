from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, PeriodForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Post
from .models import Period, Mood
from datetime import date

# Create your views here.
@login_required(login_url='/login/')
def home(request):
    return render(request, "auth/home.html")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("/MenaApp\/home")
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
