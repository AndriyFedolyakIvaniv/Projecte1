import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Choice, Question


class QuestionModelTests(TestCase):
	def test_question_string_representation(self):
		question = Question(question_text='What is new?', pub_date=timezone.now())

		self.assertEqual(str(question), 'What is new?')

	def test_recent_publication(self):
		question = Question(
			question_text='Recent question',
			pub_date=timezone.now() - datetime.timedelta(hours=23),
		)

		self.assertTrue(question.was_published_recently())

	def test_old_publication_is_not_recent(self):
		question = Question(
			question_text='Old question',
			pub_date=timezone.now() - datetime.timedelta(days=1, seconds=1),
		)

		self.assertFalse(question.was_published_recently())


class ChoiceModelTests(TestCase):
	def test_choice_defaults_to_zero_votes_and_belongs_to_question(self):
		question = Question.objects.create(
			question_text='What is new?',
			pub_date=timezone.now(),
		)
		choice = Choice.objects.create(question=question, choice_text='Nothing')

		self.assertEqual(choice.votes, 0)
		self.assertEqual(question.choice_set.get(), choice)
