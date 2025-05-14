
# from datetime import datetime, timedelta
# from django.conf import settings
# from django.contrib.auth import logout

# class SessionTimeoutMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.user.is_authenticated:
#             current_time = datetime.now()
#             last_activity = request.session.get('last_activity')

#             if last_activity:
#                 last_activity_time = datetime.fromisoformat(last_activity)
#                 inactivity_period = current_time - last_activity_time

#                 # Check if the inactivity exceeds SESSION_COOKIE_AGE
#                 if inactivity_period > timedelta(seconds=settings.SESSION_COOKIE_AGE):
#                     logout(request)

#             # Update the last activity timestamp
#             request.session['last_activity'] = current_time.isoformat()

#         response = self.get_response(request)
#         return response


from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import logout

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only enforce session timeout for authenticated users
        if request.user.is_authenticated:
            current_time = datetime.now()
            last_activity = request.session.get('last_activity')

            if last_activity:
                last_activity_time = datetime.fromisoformat(last_activity)
                inactivity_period = current_time - last_activity_time

                # Check if the inactivity exceeds SESSION_COOKIE_AGE
                if inactivity_period > timedelta(seconds=settings.SESSION_COOKIE_AGE):
                    logout(request)
                    request.session.flush()  # Completely clear session
                    return self.redirect_to_login(request)

            # Update the last activity timestamp only if user is authenticated
            request.session['last_activity'] = current_time.isoformat()

        response = self.get_response(request)
        return response

    def redirect_to_login(self, request):
        """Redirect to the login page after session expiration."""
        from django.shortcuts import redirect
        from django.urls import reverse
        return redirect(reverse('login'))  # Change 'login' to your actual login URL name