from .models import RequestLog


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # collect data on each request
        method = request.method
        path = request.path
        query_string = request.META.get("QUERY_STRING", "")
        remote_ip = request.META.get("REMOTE_ADDR", "")

        # timestamp added automatically
        RequestLog.objects.create(
            method=method, path=path, query_string=query_string, remote_ip=remote_ip
        )

        return self.get_response(request)
