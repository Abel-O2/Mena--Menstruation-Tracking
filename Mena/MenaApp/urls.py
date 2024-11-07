from django.urls import path
from . import views
from .views import register,home, logout_view, get_forum, post_forum, SymptomsView, timeOfTheMonth

urlpatterns = [
    path('home/', home, name='home'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('forum/', get_forum, name='forum'),
    path('post/', post_forum, name='post'),
    path('symptoms/', SymptomsView.as_view(), name="phase_symptoms"),
    path('calendar_view/', views.calendar_view, name='calendar_view'),
    path('calendar/', views.timeOfTheMonth ,name='period_calendar'),
]