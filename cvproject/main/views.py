from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import DetailView, ListView
from weasyprint import HTML

from .models import CV


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


class CVPDFView(DetailView):
    model = CV

    def get(self, request, *args, **kwargs):
        """
        Generates a PDF of the CV from the HTML template.
        """
        self.object = self.get_object()
        html_string = render_to_string(
            "main/cv_detail.html", {"cv": self.object, "pdf": True}
        )
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        pdf = html.write_pdf()

        response = HttpResponse(pdf, content_type="application/pdf")
        filename = f"{self.object.first_name}_{self.object.last_name}_CV.pdf"
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response
