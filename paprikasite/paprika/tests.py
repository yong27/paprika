from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from paprika.models import Board, Category, Article


class ArticleTest(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'admin@test.com', '1234')
        self.board = Board.objects.create(**{
            'type': 'blog',
            'title': 'Test board',
            'slug': 'test-board',
            'markup': 'markdown',
        })
        self.category = Category.objects.create(**{
            'title': 'My category',
            'slug': 'my-category',
        })
        self.client = Client()

    def test_create_article(self):
        self.client.login(username=self.admin.username, password=self.admin.password)
        response = self.client.post('/test-board/archive/create/', data={
            'board': self.board.id,
            'category': self.category.id,
            'title': 'This is a test article',
            'slug': 'test-article',
            'content': 'hello world',
            'tags': 'my, tags',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Article.objects.count(), 1)

