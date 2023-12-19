from django.urls import path
from article import views


urlpatterns = [
    path('articles', views.ArticlesPage, name='articles'),
    path('article/<int:pk>', views.ArticleDetail, name='article-detail'),
    path('blog', views.BlogPage, name='blog'),

    path('like_comment/<int:pk>', views.LikeComment, name='like_comment'),
    path('dislike_comment/<int:pk>', views.DislikeComment, name='dislike_comment'),
    path('complain_comment/<int:pk>', views.ComplainComment, name='complain_comment')
]
