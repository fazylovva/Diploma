from celery import shared_task
from django.core.mail import send_mail
from .models import Discussion


@shared_task
def send_warning_email(comment_id):
    comment = Discussion.objects.get(id=comment_id)
    if comment.author:
        subject = 'Warning: Comment violation'
        message = f'Your comment on {comment.article.title} has been reported by other users and may violate our ' \
                  f'community guidelines. Please review our guidelines and ensure your comments are respectful and ' \
                  f'constructive. Thank you. '
        sender = 'womenssdiary@gmail.com'
        recipient_list = [comment.author.email]
        send_mail(subject, message, sender, recipient_list)
