from django.urls import path
from analytics import views


urlpatterns = [
    path('', views.analytics_view, name='analytics'),
    path('api/discussion_likes_dislikes/', views.discussion_likes_dislikes, name='discussion_likes_dislikes'),
]