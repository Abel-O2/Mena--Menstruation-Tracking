from django.urls import path
from .views import register,home, logout_view, post_forum

urlpatterns = [
    path('home/', home, name='home'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('forum/', post_forum, name='forum'),
]