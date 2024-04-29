import datetime
from django.contrib.auth import logout
from django.http.request import HttpRequest


class SessionTimeoutMiddleware:

    time_out = 300 # en sec
    date_format = '%Y-%m-%d %H:%M:%S'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity', None)
            if last_activity:
                last_activity = datetime.datetime.strptime(last_activity, self.date_format)
                if (datetime.datetime.now() - last_activity).seconds > self.time_out:
                    logout(request)
            current_time = datetime.datetime.now().strftime(self.date_format)
            request.session['last_activity'] = current_time
        response = self.get_response(request)
        return response
    


