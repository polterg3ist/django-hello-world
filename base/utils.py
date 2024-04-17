from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator as token_generator


def is_message_valid(msg: str):
    if len(msg) > 4500:
        return False
    if not msg:
        return False
    if msg.isspace():
        return False

    return True


def send_email_for_verify(request, user, subject):
    current_site = get_current_site(request)
    context = {
        "user": user,
        "domain": current_site.domain,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": token_generator.make_token(user),
    }
    if subject.lower() == 'email':
        template_name = 'verify_email.html'
        header = 'Verify Email'
    else:
        template_name = 'verify_password.html'
        header = 'Verify password change'

    # converting template to string to send it as email
    message = render_to_string(template_name=template_name, context=context)
    email = EmailMessage(header,
                         message,
                         to=[user.email])
    email.send()

