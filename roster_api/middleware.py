import time
from .utils import ApiResponse

class TerminalLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time

        status_code = response.status_code
        method = request.method
        path = request.path

        # ANSI Colors
        BOLD = '\033[1m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        MAGENTA = '\033[95m'
        CYAN = '\033[96m'
        RESET = '\033[0m'

        # Color for status code
        if 200 <= status_code < 300:
            status_color = GREEN
        elif 300 <= status_code < 400:
            status_color = YELLOW
        elif 400 <= status_code < 500:
            status_color = RED
        else:
            status_color = MAGENTA

        # Log to terminal
        print(f"{BOLD}[{method}]{RESET} {path} - {status_color}{status_code}{RESET} ({duration:.3f}s)")

        return response
