from django.urls import path

from .views import DetailCV, ListCV

urlpatterns = [
    path("", ListCV.as_view(), name="cv-list"),
    path("<int:pk>/", DetailCV.as_view(), name="cv-detail"),
]
