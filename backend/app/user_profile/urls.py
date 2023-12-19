from django.urls import path
from .views import UserProfile, EditProfile


urlpatterns = [
    path('', UserProfile, name='profile'),
    path('edit', EditProfile, name='edit_profile'),
]
