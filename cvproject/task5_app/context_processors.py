from django.conf import settings


def settings_context(request):
    """
    unsafe, but it's just a demo for test task
    """
    return {"settings": settings}
