from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_password_reset_email(email, reset_url):
    send_mail(
        subject="Growthness - Password Reset Request",
        message=f"Use the following link to reset your password: {reset_url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
    )
