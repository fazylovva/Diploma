from django.db import models
from account.models import User
from ckeditor.fields import RichTextField


class ArticleAdmin(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/articles/', null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    summary = models.TextField()
    description = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.image_url = f'http://localhost:8000/media/images/articles/{self.image.name}'
        super().save(*args, **kwargs)

    def formatted_date(self):
        return self.created_date.strftime("%B %d, %Y")

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Article Admin'


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/articles/', null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    summary = models.TextField()
    description = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.image_url = f'http://localhost:8000/media/images/articles/{self.image.name}'
        super().save(*args, **kwargs)

    def formatted_date(self):
        return self.created_date.strftime("%B %d, %Y")

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Article'


class Discussion(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, related_name='article_discussion')
    comment = models.TextField()
    is_anonymous = models.BooleanField(default=False)
    like = models.ManyToManyField(User, related_name='like_comment', null=True, blank=True)
    dislike = models.ManyToManyField(User, related_name='dislike_comment', null=True, blank=True)
    complain = models.ManyToManyField(User, related_name='complain_comment', null=True, blank=True)

    def __str__(self):
        return f'Author: {self.author} <---> Comment: {self.comment}'

    class Meta:
        db_table = 'Discussion'


class ViewedArticle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    viewed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User: {self.user} <---> Article: {self.article}'

    class Meta:
        db_table = 'Viewed Article'
