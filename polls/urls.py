from django.urls import path

from . import views

urlpatterns = [
    # Ex: /polls/
    path("", views.index, name="index"),
    # Ex: /polls/5/
    path("<int:question_id>/", views.detail, name="detail"),
    # Ex: /polls/5/results/
    path("<int:question_id>/results/", views.results, name="results"),
    # Ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
