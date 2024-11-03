from django.urls import path
from .views import register,home, logout_view, forums

urlpatterns = [
    path('home/', home, name='home'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('forums/', forums, name='forums'),
]