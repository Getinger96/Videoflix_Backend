import os
from email.mime.base import MIMEBase
from email import encoders
from django.conf import settings
from django.utils.encoding import force_bytes, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


def _build_email_context(user, token):
    return {
        'user': user,
        'frontend_url': settings.FRONTEND_URL,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token,
    }


def _attach_logo(email):
    logo_path = os.path.join(settings.BASE_DIR, 'email_assets', 'logo_icon.svg')
    with open(logo_path, 'rb') as f:
        logo = MIMEBase('image', 'svg+xml')
        logo.set_payload(f.read())
        encoders.encode_base64(logo)
        logo.add_header('Content-ID', '<logo_image>')
        logo.add_header('Content-Disposition', 'inline', filename='logo_icon.svg')
        email.attach(logo)


def _send_activation_email(user, token, to_email):
    context = _build_email_context(user, token)
    html_content = render_to_string('acc_active_email.html', context)
    text_content = render_to_string('acc_active_email.txt', context)

    email = EmailMultiAlternatives(
        subject='Confirmation message',
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email]
    )
    email.attach_alternative(html_content, "text/html")
    _attach_logo(email)
    email.send()


def _send_token_email(user, token, subject, html_template, txt_template):
    context = _build_email_context(user, token)
    html_content = render_to_string(html_template, context)
    text_content = render_to_string(txt_template, context)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email]
    )
    email.attach_alternative(html_content, "text/html")
    _attach_logo(email)
    email.send()