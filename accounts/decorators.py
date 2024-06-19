from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied

def unauthenticated_user(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        else:
            return view_func(request, *args, **kwargs)
    return wrap


def student_only(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_warden:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))
    return wrap

def warden_only(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_warden:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('student_land'))
    return wrap