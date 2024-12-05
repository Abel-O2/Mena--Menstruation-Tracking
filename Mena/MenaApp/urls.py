from django.urls import path
from .views import register,home, logout_view, post_forum
from . import views
from .views import register,home, logout_view, get_forum, post_forum

urlpatterns = [
    path('home/', home, name='home'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('forum/', get_forum, name='forum'),
    path('forum/post/', post_forum, name='post'),
    path('forum/delete/<int:id>/', views.delete_forum, name='delete_post'),
    path('forum/edit/<int:id>/', views.edit_forum, name='edit_post'),
    path('comment/add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('comment/edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('comment/delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('calendar/<int:year>/<int:month>/', views.calendar_view, name='calendar_view'),
    path('period/', views.period_tracker, name='period_tracker'),
    path('edit-period/<int:period_id>/', views.edit_period, name='edit_period'),
]