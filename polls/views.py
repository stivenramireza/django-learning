from django.shortcuts import render
from django.http import HttpResponse


def index(request: object) -> None:
    return HttpResponse("Hello world!")
