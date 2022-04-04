from cgitb import text
import datetime
from venv import create

from django.test import TestCase
from django.utils import timezone
from django.urls.base import reverse

from .models import Question


def create_question(text: str, days: int) -> Question:
    """
    Creates a question with the given text and days. Remember that positive
    days is applied to future questions and negative days to past questions.

    Args:
        text: Description of the question.
        days: Number of days in the future or past.

    Returns:
        The created question in the database.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    question = Question.objects.create(question_text=text, pub_date=time)
    return question


class TestQuestionModel(TestCase):
    def test_was_published_recently_with_future_questions(self) -> None:
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        future_question = create_question(text="Future question", days=30)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_present_questions(self) -> None:
        """
        was_published_recently() returns True for questions whose pub_date is
        in the present.
        """
        present_question = create_question(text="Present question", days=0)
        self.assertIs(present_question.was_published_recently(), True)

    def test_was_published_recently_with_past_questions(self) -> None:
        """
        was_published_recently() returns False for questions whose pub_date is
        in the present.
        """
        past_question = create_question(text="Past question", days=-15)
        self.assertIs(past_question.was_published_recently(), False)


class TestQuestionIndexView(TestCase):
    def test_no_questions(self) -> None:
        """
        If no question exists, an appropiate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_questions(self) -> None:
        """
        If future questions are present, they won't display in the page.
        """
        create_question(text="Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_questions(self) -> None:
        """
        If future questions are present, they won't display in the page.
        """
        past_question = create_question(text="Past question", days=-7)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["latest_question_list"], [past_question]
        )

    def test_future_and_past_questions(self) -> None:
        """
        Even if both past and future questions exist, only past questions are displayed.
        """
        past_question = create_question(text="Past question", days=-4)
        create_question(text="Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"], [past_question]
        )

    def test_two_past_questions(self) -> None:
        """
        The questions index page may display multiple questions.
        """
        past_question_1 = create_question(text="Past question 1", days=-4)
        past_question_2 = create_question(text="Past question 2", days=-8)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["latest_question_list"], [past_question_1, past_question_2]
        )

    def test_two_future_questions(self) -> None:
        create_question(text="Future question 1", days=9)
        create_question(text="Future question 2", days=21)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
