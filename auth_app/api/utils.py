
from django.conf import settings
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from email.mime.base import MIMEBase
from email import encoders
import os
from django.utils.http import urlsafe_base64_encode

def _build_email_context(user, token):
    """
    Build the template context for email rendering.

    :param user: The user object the email is addressed to
    :param token: The secure one-time token for the email link
    :return: Dictionary containing user, frontend_url, uid and token
    """
    return {
        'user': user,
        'frontend_url': settings.FRONTEND_URL,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token,
    }


def _attach_logo(email):
    """
    Attach the company logo as an inline SVG to the given email.

    Reads the logo file from the email_assets directory and attaches
    it with a Content-ID header so it can be referenced in HTML templates
    via cid:logo_image.

    :param email: The EmailMultiAlternatives object to attach the logo to
    """
    logo_path = os.path.join(settings.BASE_DIR, 'email_assets', 'logo_icon.svg')
    with open(logo_path, 'rb') as f:
        logo = MIMEBase('image', 'svg+xml')
        logo.set_payload(f.read())
        encoders.encode_base64(logo)
        logo.add_header('Content-ID', '<logo_image>')
        logo.add_header('Content-Disposition', 'inline', filename='logo_icon.svg')
        email.attach(logo)


def _send_activation_email(user, token, to_email):
    """
    Send an account activation email to a newly registered user.

    Renders both HTML and plain text versions of the activation email
    and sends them with the company logo attached inline.

    :param user: The user object to activate
    :param token: The secure activation token
    :param to_email: The recipient's email address
    """
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
    """
    Send a generic token-based email (e.g. password reset, activation).

    Renders both HTML and plain text versions using the provided templates
    and sends them with the company logo attached inline.

    :param user: The user object the email is addressed to
    :param token: The secure one-time token for the email link
    :param subject: The email subject line
    :param html_template: Path to the HTML template file
    :param txt_template: Path to the plain text template file
    """
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