from aistocks import settings
from django.contrib.auth.models import User
from celery import shared_task
from django.core.mail import send_mail
@shared_task(bind=True)
def send_mails(self):
    users = User.objects.all()
    mail_subject = 'hi am rajat'
    message = 'how are you'
    for user in users:
        to_email=user.email
        send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True
        )
    return 'done'