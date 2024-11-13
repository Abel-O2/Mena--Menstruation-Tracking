from django.urls import path
from .views import register,home, logout_view, post_forum
from . import views

urlpatterns = [
    path('home/', home, name='home'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('forum/', post_forum, name='forum'),
    path('period/', views.period_tracker, name='period_tracker'),
    path('edit-period/<int:period_id>/', views.edit_period, name='edit_period'),
]