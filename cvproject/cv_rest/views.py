# views.py
from main.models import CV
from rest_framework import viewsets

from .serializers import CVSerializer


class CVViewSet(viewsets.ModelViewSet):
    # ModelViewSet used to minimize required time to provide basic crud functionality
    queryset = CV.objects.all()
    serializer_class = CVSerializer
