from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML


def generate_cv_pdf(cv, request):
    """
    Generates a PDF for a given CV instance.
    """
    html_string = render_to_string("main/cv_detail.html", {"cv": cv, "pdf": True})
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type="application/pdf")
    filename = f"{cv.first_name}_{cv.last_name}_CV.pdf"
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response
