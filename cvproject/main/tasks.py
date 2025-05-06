from __future__ import absolute_import, unicode_literals

from io import BytesIO

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from djcelery_email.backends import CeleryEmailBackend

from .models import CV
from .utils import generate_cv_pdf


@shared_task
def send_cv_pdf_to_email(cv_id, recipient_email):
    """
    Celery task that generates a PDF of the CV and sends it to the given email.
    """
    cv = CV.objects.get(id=cv_id)

    from django.http import HttpRequest

    request = HttpRequest()
    request.build_absolute_uri = lambda: "http://localhost:8000"

    response = generate_cv_pdf(cv, request)

    pdf_content = BytesIO(response.content)

    email_subject = f"{cv.first_name} {cv.last_name} - CV"
    email_body = "Please find the attached CV PDF."

    email = EmailMessage(
        subject=email_subject,
        body=email_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient_email],
    )

    email.attach(
        f"{cv.first_name}_{cv.last_name}_CV.pdf",
        pdf_content.getvalue(),
        "application/pdf",
    )

    email.backend = CeleryEmailBackend()
    email.send()

    return f"PDF sent to {recipient_email}"
