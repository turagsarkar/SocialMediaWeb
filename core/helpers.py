from email import message
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile


def forget_pass_sendmail(email,token):
    
    subject = "Reset Password"
    message = f'Click This Link to reset your Password:  http://127.0.0.1:8000/resetPassword/{token}/'
    email_from = settings.EMAIL_HOST_USER   
    recipient_list = [email]
    send_mail(subject,message,email_from,recipient_list)
    return True

def verify_account_sendmail(email,token):
    subject = "Activate Your Account"
    message = f'Click This Link to activate your account:  http://127.0.0.1:8000/verify_email/{token}/'
    email_from = settings.EMAIL_HOST_USER   
    recipient_list = [email]
    send_mail(subject,message,email_from,recipient_list)
    return True