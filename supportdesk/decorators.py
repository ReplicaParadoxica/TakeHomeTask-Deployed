from django.http import HttpResponse
from django.shortcuts import redirect


def customers_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_staff:
            return redirect('request_list')
        return view_func(request, *args, **kwargs)
    return wrapper_func


def agents_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('request_list')
        return view_func(request, *args, **kwargs)
    return wrapper_func
