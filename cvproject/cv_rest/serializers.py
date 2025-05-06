from main.models import CV
from rest_framework import serializers


class CVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CV
        fields = "__all__"
