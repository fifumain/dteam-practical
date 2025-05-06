from django.views.generic import DetailView, ListView

from .models import CV
from .utils import generate_cv_pdf


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


from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView

from .models import CV
from .tasks import send_cv_pdf_to_email  # Import the Celery task


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

            return HttpResponseRedirect(reverse("cv-list"))

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
