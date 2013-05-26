from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from paprika.models import Board, Category, Article, Tag
from paprika.views.article import ArticleForm


class ArticleTest(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 
                'admin@test.com', '1234')
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
        self.form_data = {
            'board': self.board.id,
            'category': self.category.id,
            'title': 'This is a test article',
            'slug': 'test-article',
            'content': 'hello world',
            'custom_tags': 'my, tags',
            'registrator': self.admin.id,
            }
        self.client = Client()

    def test_article_form(self):
        form = ArticleForm(data=self.form_data)
        self.assertEqual(form.is_valid(), True)

    def test_create_article(self):
        self.client.login(username='admin', password='1234')
        response = self.client.post('/test-board/archive/create/', self.form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://testserver/1/test-article/')
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Tag.objects.count(), 2)

    def test_update_article(self):
        self.client.login(username='admin', password='1234')
        self.client.post('/test-board/archive/create/', self.form_data)

        new_form_data = self.form_data.copy()
        new_form_data.update(content='hello python')
        response = self.client.post('/1/test-article/update/', new_form_data)
        self.assertEqual(Article.objects.get(id=1).content, 'hello python')

    def test_update_tags(self):
        self.client.login(username='admin', password='1234')
        self.client.post('/test-board/archive/create/', self.form_data)

        new_form_data = self.form_data.copy()
        new_form_data.update(custom_tags='my, world')
        response = self.client.post('/1/test-article/update/', new_form_data)

        article = Article.objects.get(id=1)
        self.assertEqual(set(t.slug for t in article.tags.all()), 
                set(['my', 'world']))
        self.assertEqual(set(t.slug for t in Tag.objects.all()), 
                set(['my', 'world']))

    def test_publish_article(self):
        self.client.login(username='admin', password='1234')
        self.client.post('/test-board/archive/create/', self.form_data)
        self.client_guest = Client()

        # guest can not see the content
        response = self.client_guest.get('/1/test-article/')
        self.assertEqual('hello world' in str(response.content), False)
        # admin can see the content
        response = self.client.get('/1/test-article/')
        self.assertEqual('hello world' in str(response.content), True)

        # after publish, guest can see the content
        self.client.post('/1/test-article/publish/', {'publish': 'true'})
        response = self.client_guest.get('/1/test-article/')
        self.assertEqual('hello world' in str(response.content), True)
        # after unpublish, guest can not see the content
        self.client.post('/1/test-article/publish/', {'publish': 'false'})
        response = self.client_guest.get('/1/test-article/')
        self.assertEqual('hello world' in str(response.content), False)

