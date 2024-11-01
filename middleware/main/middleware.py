import os

from django.utils.timezone import now


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        method = request.method
        url = request.get_full_path()
        username = request.user.username if request.user.is_authenticated else 'notfind'


        log_file_name = f"{username or ip}.log"
        log_file_path = os.path.join('logs', log_file_name)


        with open(log_file_path, 'a') as log_file:
            log_file.write(f"[{now()}] {method} {url} from {ip}\n")

        response = self.get_response(request)


        with open(log_file_path, 'a') as log_file:
            log_file.write(f"[{now()}] status: {response.status_code}\n")

        return response
