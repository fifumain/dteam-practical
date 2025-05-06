from django.urls import path

from .views import recent_logs_view

urlpatterns = [
    path("logs/", recent_logs_view, name="recent-logs"),
]
