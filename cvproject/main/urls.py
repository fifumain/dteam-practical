from django.urls import path

from .views import CVPDFView, DetailCV, ListCV

urlpatterns = [
    path("", ListCV.as_view(), name="cv-list"),
    path("<int:pk>/", DetailCV.as_view(), name="cv-detail"),
    path("cv/<int:pk>/download/", CVPDFView.as_view(), name="cv-pdf"),
]
