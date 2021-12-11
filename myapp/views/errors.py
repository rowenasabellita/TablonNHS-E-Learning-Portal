from django.http.response import HttpResponseServerError
from django.shortcuts import redirect, render
from django.http import HttpResponse


def internal_server_error(request, redirect_to):
    return render(request, 'internal_server_error.html', {"redirect_to": "/{}".format(redirect_to), "error_msg": ""})
