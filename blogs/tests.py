import os

import django
from django.http import Http404
from django.test import TestCase

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")
django.setup()

from .models import Topic
from .utils import get_topics, check_topic_owner
from django.contrib.auth import get_user_model
# Create your tests here.

class TestTopics(TestCase):
    def test_topics(self):
        user = get_user_model().objects.create_user('testuser', 'test@email.com', '12345')
        self.client.login(username='testuser', password='12345')
        Topic(text='Test', owner=user).save()
        response = self.client.get('/topics/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_topic(self):
        user = get_user_model().objects.create_user('testuser', 'test@email.com', '12345')
        self.client.login(username='testuser', password='12345')
        topic = Topic(text='Test Topic', owner=user)
        topic.save()
        response = self.client.post(f"/topics/{topic.id}/", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_get_topics(self):
        user = get_user_model().objects.create_user('testuser', 'test@email.com', '12345')
        topic = Topic(text='Test', owner=user)
        topic.save()
        topics = get_topics(user)
        self.assertEqual(list(topics), [topic])

    def test_check_topic_owner(self):
        user = get_user_model().objects.create_user('testuser', 'test@email.com', '12345')
        user1 = get_user_model().objects.create_user('testuser1', 'test1@email.com', '123456')
        self.client.login(username='testuser', password='12345')
        topic = Topic(text='Test', owner=user1)
        response = self.client.post(f"/topics/{topic.id}/", follow=True)
        request = response.wsgi_request
        self.assertRaises(Http404, '', '')

    def test_check_topic_owner(self):
        user = get_user_model().objects.create_user('testuser', 'test@email.com', '12345')
        self.client.login(username='testuser', password='12345')
        topic = Topic(text='Test', owner=user)
        response = self.client.post(f"/topics/{topic.id}/", follow=True)
        request = response.wsgi_request
        self.assertEqual(check_topic_owner(request, topic), None)