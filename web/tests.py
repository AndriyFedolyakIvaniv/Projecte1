import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

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


class QuestionViewTests(TestCase):
	def test_index_displays_latest_five_questions(self):
		for question_number in range(6):
			Question.objects.create(
				question_text=f'Question {question_number}',
				pub_date=timezone.now() + datetime.timedelta(minutes=question_number),
			)

		response = self.client.get(reverse('web:index'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Question 5')
		self.assertNotContains(response, 'Question 0')

	def test_index_shows_empty_message_without_questions(self):
		response = self.client.get(reverse('web:index'))

		self.assertContains(response, 'No questions are available.')

	def test_detail_displays_question_and_choices(self):
		question = Question.objects.create(
			question_text='What is new?',
			pub_date=timezone.now(),
		)
		Choice.objects.create(question=question, choice_text='Nothing')

		response = self.client.get(reverse('web:detail', args=[question.pk]))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'What is new?')
		self.assertContains(response, 'Nothing')

	def test_detail_returns_not_found_for_unknown_question(self):
		response = self.client.get(reverse('web:detail', args=[999]))

		self.assertEqual(response.status_code, 404)

	def test_results_and_vote_views_include_question_id(self):
		results_response = self.client.get(reverse('web:results', args=[7]))
		vote_response = self.client.get(reverse('web:vote', args=[7]))

		self.assertContains(results_response, 'results of question 7')
		self.assertContains(vote_response, 'voting on question 7')
