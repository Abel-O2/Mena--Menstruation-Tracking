from django.urls import path
<<<<<<< HEAD
from .views import register,home, logout_view, post_forum
from . import views
=======
from . import views
from .views import register,home, logout_view, get_forum, post_forum, SymptomsView, timeOfTheMonth
>>>>>>> eadd848fada6845d4b234a6b0c7b7e9124a14556

urlpatterns = [
    path('home/', home, name='home'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
<<<<<<< HEAD
    path('forum/', post_forum, name='forum'),
    path('period/', views.period_tracker, name='period_tracker'),
    path('edit-period/<int:period_id>/', views.edit_period, name='edit_period'),
=======
    path('forum/', get_forum, name='forum'),
    path('post/', post_forum, name='post'),
    path('symptoms/', SymptomsView.as_view(), name="phase_symptoms"),
    path('calendar_view/', views.calendar_view, name='calendar_view'),
    path('calendar/', views.timeOfTheMonth ,name='period_calendar'),
>>>>>>> eadd848fada6845d4b234a6b0c7b7e9124a14556
]