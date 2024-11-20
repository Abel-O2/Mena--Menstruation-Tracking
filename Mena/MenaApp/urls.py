from django.urls import path
from .views import register,home, logout_view, post_forum
from . import views
from .views import register,home, logout_view, get_forum, post_forum, SymptomsView, timeOfTheMonth, calendar_view

urlpatterns = [
    path('home/', home, name='home'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('forum/', post_forum, name='forum'),
    path('period/', views.period_tracker, name='period_tracker'),
    path('edit-period/<int:period_id>/', views.edit_period, name='edit_period'),
    path('forum/', get_forum, name='forum'),
    path('forum/post/', post_forum, name='post'),
    path('forum/delete/<int:id>/', views.delete_forum, name='delete_post'),
    path('forum/edit/<int:id>/', views.edit_forum, name='edit_post'),
    path('symptoms/', SymptomsView.as_view(), name="phase_symptoms"),
    path('calendar_view/', views.calendar_view, name='calendar_view'),
    path('calendar/', views.timeOfTheMonth ,name='period_calendar'),

    path('calendar/', calendar_view, name='calendar_view'),
    path('calendar/data/', timeOfTheMonth ,name='time_of_the_month'),
]