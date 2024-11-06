from django.urls import path
from .views import register,home, logout_view, post_forum, SymptomsView

urlpatterns = [
    path('home/', home, name='home'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('forum/', post_forum, name='forum'),
    path('symptoms/', SymptomsView.as_view(), name="phase_symptoms"),
]