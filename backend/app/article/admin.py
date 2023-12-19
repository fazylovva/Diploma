from django.contrib import admin
from .models import ArticleAdmin, Article, Discussion, ViewedArticle


admin.site.register(ArticleAdmin)
admin.site.register(Article)
admin.site.register(Discussion)
admin.site.register(ViewedArticle)
