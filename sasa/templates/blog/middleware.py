# middleware.py

from django.utils import timezone
from datetime import timedelta

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'last_activity' in request.session:
            if timezone.now() - request.session['last_activity'] > timedelta(minutes=30):
                request.session.flush()
        request.session['last_activity'] = timezone.now()
        response = self.get_response(request)
        return response
