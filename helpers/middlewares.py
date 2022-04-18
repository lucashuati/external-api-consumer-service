import logging


class ResponseLogMiddleware:
    def get_log_level(self, status_code):
        if status_code < 400:
            return "info"
        if status_code < 500:
            return "warning"

        return "error"

    def log(self, response):
        logger = logging.getLogger("response")
        log_level = self.get_log_level(response.status_code)
        log_level_method = getattr(logger, log_level)
        log_level_method(
            {
                "content": response.content,
                "status_code": response.status_code,
            }
        )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        self.log(response)
        return response
