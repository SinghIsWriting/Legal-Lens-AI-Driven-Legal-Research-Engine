from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

def send_welcome_email(user, email):
    subject = 'Welcome to AI Legal Support'
    html_message = render_to_string('legalSupport/welcome_email.html', {'user': user})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to = email

    msg = EmailMultiAlternatives(subject, plain_message, from_email, [to])
    msg.attach_alternative(html_message, "text/html")
    msg.send()