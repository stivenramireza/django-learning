from cgitb import text
import datetime
from venv import create

from django.test import TestCase
from django.utils import timezone
from django.urls.base import reverse

from .models import Question, Choice


def create_question(text: str, days: int, with_choices: bool = True) -> Question:
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
    question = Question(question_text=text, pub_date=time)
    choice_a = Choice(question=question, choice_text="Option A", votes=0)
    choice_b = Choice(question=question, choice_text="Option B", votes=0)
    choices = [choice_a, choice_b] if with_choices else []
    question.save(choices=choices)
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

    # def test_question_without_choices(self) -> None:
    #    """
    #    If the question don't have choices, it raises an Exception.
    #    """
    #    with self.assertRaisesRegex(
    #        Exception, "Question must have at least one choice"
    #    ):
    #        create_question(text="Present question", days=0, with_choices=False)


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
        """
        The question index page won't display questions because it
        contains only future questions.
        """
        create_question(text="Future question 1", days=9)
        create_question(text="Future question 2", days=21)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["latest_question_list"], [])


class TestQuestionDetailView(TestCase):
    def test_future_question(self) -> None:
        """
        The detail view of a question with a pub_date in the future
        returns a 404 error not found.
        """
        future_question = create_question(text="Future question", days=20)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self) -> None:
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(text="Past question", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class TestQuestionResultView(TestCase):
    def test_not_question(self) -> None:
        """
        The result view of a inexistent question, it will display an
        404 error not found page.
        """
        inexistent_question_id = 1000
        url = reverse("polls:results", args=(inexistent_question_id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_future_question(self) -> None:
        """
        The result view of a question with a pub_date in the future
        returns a 404 error not found.
        """
        future_question = create_question(text="Future question", days=5)
        url = reverse("polls:results", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
