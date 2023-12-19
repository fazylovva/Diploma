from django.db.models.signals import pre_save
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from article.models import Article


@receiver(post_save, sender=Article)
def send_post_notification(sender, instance, created, **kwargs):
    if created:
        subject = 'Your article has been added to our site'
        message = render_to_string('article/article_notification.html', {'article': instance})
        from_email = 'womenssdiary@gmail.com'
        to_email = [instance.author.email]
        send_mail(subject, message, from_email, to_email, html_message=message)
