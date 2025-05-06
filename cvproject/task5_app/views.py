from django.shortcuts import render


def settings_view(request):
    return render(request, "task5_app/settings.html")
