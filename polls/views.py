from django.shortcuts import render
from django.http import HttpResponse


def index(request: object) -> object:
    return HttpResponse("You are in the main page")


def detail(request: object, question_id: int) -> object:
    return HttpResponse(f"You are watching the question #{question_id}")


def results(request: object, question_id: int) -> object:
    return HttpResponse(f"You are watching the results of the question #{question_id}")


def results(request: object, question_id: int) -> object:
    return HttpResponse(f"You are voting the question #{question_id}")
