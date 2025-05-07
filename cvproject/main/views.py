import os

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import DetailView, ListView
from openai import OpenAI

from .models import CV
from .tasks import send_cv_pdf_to_email
from .utils import generate_cv_pdf

client = OpenAI(
    api_key=os.getenv("OPENAI_KEY"),
)


class ListCV(ListView):
    model = CV
    template_name = "main/cv_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Adds extra variables to context (dictionary) that are passed to a template.
        Used to set title of page.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "CV List"
        return context

    def get_queryset(self):
        return CV.objects.order_by("-created_at")


class DetailCV(DetailView):
    model = CV
    template_name = "main/cv_detail.html"
    context_object_name = "cv"

    def post(self, request, *args, **kwargs):
        """
        Handles the POST request to send the CV PDF to the provided email.
        """
        cv = self.get_object()
        recipient_email = request.POST.get("email")

        if recipient_email:

            send_cv_pdf_to_email.delay(cv.id, recipient_email)

            return HttpResponseRedirect(reverse("cv-list-home"))

        return render(
            request,
            self.template_name,
            {"cv": cv, "error": "Please provide a valid email."},
        )


class CVPDFView(DetailView):
    model = CV

    def get(self, request, *args, **kwargs):
        """
        Generates a PDF of the CV from the HTML template using the utility function.
        """
        self.object = self.get_object()
        return generate_cv_pdf(self.object, request)


def translate_cv(request, cv_id):
    cv = get_object_or_404(CV, id=cv_id)

    translated_bio = None
    translated_contacts = None
    translated_skills = None
    translated_projects = None

    if request.method == "POST":
        selected_language = request.POST.get("language")

        # Translate the content fields
        translated_bio = translate_with_openai(cv.bio, selected_language)
        translated_contacts = translate_with_openai(cv.contacts, selected_language)
        translated_skills = translate_with_openai(cv.skills, selected_language)
        translated_projects = translate_with_openai(cv.projects, selected_language)

        return render(
            request,
            "main/cv_detail.html",
            {
                "cv": cv,
                "translated_bio": translated_bio,
                "translated_contacts": translated_contacts,
                "translated_skills": translated_skills,
                "translated_projects": translated_projects,
                "language": selected_language,
            },
        )

    return render(request, "main/cv_detail.html", {"cv": cv})


def translate_with_openai(cv_text, target_language):
    """Function for translating text using OpenAI API"""
    try:
        # API request
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Help me translate text."},
                {
                    "role": "user",
                    "content": f"Translate the following text to {target_language}: {cv_text}. Give me only translated text, nothing else.",
                },
            ],
        )

        # Extract the translated text from the response
        translated_text = response.choices[0].message.content.strip()
        return translated_text

    except Exception as e:
        return f"Error during translation: {e}"
