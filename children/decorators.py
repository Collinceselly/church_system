from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse


def custom_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            # # Check if user has a 'role' attribute
            # if hasattr(request.user, 'is_staff') and request.user.is_staff:
            #     return redirect('/user/login/')
            # else:
            #     return redirect('/member/login/')
            return redirect('/')

        return view_func(request, *args, **kwargs)

    return _wrapped_view
