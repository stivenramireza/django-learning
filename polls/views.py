from django.shortcuts import render
from django.http import HttpResponse

from .models import Question


def index(request: object) -> object:
    latest_question_list = Question.objects.all()
    return render(
        request, "polls/index.html", {"latest_question_list": latest_question_list}
    )


def detail(request: object, question_id: int) -> object:
    return HttpResponse(f"You are watching the question #{question_id}")


def results(request: object, question_id: int) -> object:
    return HttpResponse(f"You are watching the results of the question #{question_id}")


def vote(request: object, question_id: int) -> object:
    return HttpResponse(f"You are voting the question #{question_id}")
