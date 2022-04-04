import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question


class TestQuestionModel(TestCase):
    def setUp(self) -> None:
        self.question = Question(
            question_text="¿Quién es el mejor Course Director de Platzi?"
        )

    def test_was_published_recently_with_future_questions(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        self.question.pub_date = timezone.now() + datetime.timedelta(days=30)
        self.assertIs(self.question.was_published_recently(), False)

    def test_was_published_recently_with_present_questions(self):
        """
        was_published_recently() returns True for questions whose pub_date is
        in the present.
        """
        self.question.pub_date = timezone.now()
        self.assertIs(self.question.was_published_recently(), True)

    def test_was_published_recently_with_past_questions(self):
        """
        was_published_recently() returns True for questions whose pub_date is
        in the present.
        """
        self.question.pub_date = timezone.now() - datetime.timedelta(days=30)
        self.assertIs(self.question.was_published_recently(), False)
