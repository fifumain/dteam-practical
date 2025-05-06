from django.urls import path

from .views import CVPDFView, DetailCV, ListCV

urlpatterns = [
    path("", ListCV.as_view(), name="cv-list"),
    path("<int:pk>/", DetailCV.as_view(), name="cv-detail"),
    path("<int:pk>/send-pdf/", DetailCV.as_view(), name="send_pdf_to_email"),
    path("<int:pk>/pdf/", CVPDFView.as_view(), name="cv-pdf"),
]
