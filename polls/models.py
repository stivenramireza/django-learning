import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField("Question text", max_length=200)
    pub_date = models.DateTimeField("Published date")

    def __str__(self) -> str:
        return self.question_text

    def was_published_recently(self) -> bool:
        return (
            timezone.now()
            >= self.pub_date
            >= timezone.now() - datetime.timedelta(days=1)
        )

    def save(self, choices: list[object] = None, *args, **kwargs) -> None:
        question = super().save(*args, **kwargs)
        # TODO Check the correct way to do this
        # if not choices:
        #     raise Exception("Question must have at least one choice")
        # for choice in choices:
        #     choice.save
        return question


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField("Choice text", max_length=200)
    votes = models.IntegerField("Votes", default=0)

    def __str__(self) -> str:
        return self.choice_text
