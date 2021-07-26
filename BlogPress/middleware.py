from django.conf import settings
from django.shortcuts import redirect

class URLMiddleware:
    #first
    def __init__(self, get_response):
        self.get_response = get_response
    #second
    def __call__(self, request):
        response = self.get_response(request)
        return response
    #third
    def process_view(self, request, view_func, view_args, view_kwargs):

        # if user is authenticated and on home_url, then logout
        user = request.user.is_authenticated
        url = request.path
        if user and url in settings.EXEMPT_URLS:
            return redirect("/")