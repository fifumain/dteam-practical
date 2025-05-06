from django.views.generic import DetailView, ListView

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
