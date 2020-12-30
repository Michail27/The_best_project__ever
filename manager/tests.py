from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from slugify import slugify

from manager.models import Book, Comment, LikeCommentUser


class TestMyAppPlease(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user('test_name')
        self.user1 = User.objects.create_user('test_name1')
        self.user2 = User.objects.create_user('test_name2')

    def test_add_book(self):
        self.client.force_login(self.user)
        url = reverse('add-book')
        data = {
            'title': 'test title',
            'text': 'test text'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302, msg='is not redirect')
        self.assertTrue(Book.objects.exists(), msg='book is not created')
        book = Book.objects.first()
        self.assertEqual(book.title, data['title'])
        self.assertEqual(book.text, data['text'])
        self.assertEqual(book.slug, slugify(data['title']))
        self.assertEqual(book.__str__(), 'test title - test-title')
        self.assertEqual(book.authors.first(), self.user)
        self.client.logout()
        data = {
            'title': 'test title',
            'text': 'test text'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302, msg='is not redirect')
        self.assertEqual(Book.objects.count(), 1,  msg='created book without author')

    def test_except_slug(self):
        self.client.force_login(self.user)
        self.book1 = Book.objects.create(title='test_title1')
        self.book1.authors.add(self.user)
        self.book1.save()
        data = {
            'title': 'test-title2',
            'text': 'test-text'
        }
        url = reverse('update-book', kwargs=dict(slug=self.book1.slug))
        response = self.client.post(url, data)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, data['title'], msg='book1 is not refreshed')
        self.assertEqual(self.book1.text, data['text'], msg='book1 is not refreshed')
        self.book2 = Book.objects.create(title='test_title1')
        self.assertNotEqual(self.book2.slug, 'test_title1')

    def test_update_book(self):
        self.client.force_login(self.user)
        self.book1 = Book.objects.create(title='test_title1')
        self.book1.authors.add(self.user)
        self.book1.save()
        self.book2 = Book.objects.create(title='test_title2')
        self.book2.authors.add(self.user)
        self.book2.save()
        self.assertEqual(Book.objects.count(), 2)
        data = {
            'title': 'test title',
            'text': 'test text'
        }
        url = reverse('update-book', kwargs=dict(slug=self.book1.slug))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, data['title'], msg='book1 is not refreshed')
        self.assertEqual(self.book1.text, data['text'], msg='book1 is not refreshed')
        self.assertEqual(self.book1.authors.first(), self.user)
        self.client.logout()
        url = reverse('update-book', kwargs=dict(slug=self.book2.slug))
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.book2.refresh_from_db()
        self.assertNotEqual(self.book2.title, data['title'])
        self.assertNotEqual(self.book2.text, data['text'])
        self.client.logout()
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.book2.refresh_from_db()
        self.assertNotEqual(self.book2.title, data['title'])
        self.assertNotEqual(self.book2.text, data['text'])

    def test_rate_book(self):
        self.client.force_login(self.user)
        self.book1 = Book.objects.create(title='test_title1')
        url = reverse('add-rate', kwargs=dict(slug=self.book1.slug, rate=3))
        self.client.get(url)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.rate, 3)
        # new user
        self.client.force_login(self.user1)
        url = reverse('add-rate', kwargs=dict(slug=self.book1.slug, rate=4))
        self.client.get(url)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.rate, 3.5)
        # next user
        self.client.force_login(self.user2)
        url = reverse('add-rate', kwargs=dict(slug=self.book1.slug, rate=5))
        self.client.get(url)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.rate, 4)

        self.client.force_login(self.user)
        url = reverse('add-rate', kwargs=dict(slug=self.book1.slug, rate=5))
        self.client.get(url)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.rate, Decimal('4.67'))

    def test_book_delete(self):
        self.client.force_login(self.user)
        self.book1 = Book.objects.create(title='test_title1')
        self.book1.authors.add(self.user)
        self.book1.save()
        self.book2 = Book.objects.create(title='test_title2')
        self.assertEqual(Book.objects.count(), 2)
        url = reverse('del-book', kwargs=dict(slug=self.book1.slug))
        self.client.get(url)
        self.assertEqual(Book.objects.count(), 1)
        url = reverse('del-book', kwargs=dict(slug=self.book2.slug))
        self.client.get(url)
        self.assertEqual(Book.objects.count(), 1)
        self.client.logout()
        self.client.get(url)
        self.assertEqual(Book.objects.count(), 1)

    def test_add_comment(self):
        self.client.force_login(self.user)
        self.book1 = Book.objects.create(title='test_title1')
        url = reverse('add-comment', kwargs=dict(slug=self.book1.slug))
        data = {
             'text': 'test text'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302, msg='is not redirect')
        self.assertTrue(Comment.objects.exists(), msg='Comment is not created')
        comment = Comment.objects.first()
        self.assertEqual(comment.text, data['text'])
        self.assertEqual(comment.book, self.book1, msg='comment bellong to Book')
        self.assertEqual(comment.author, self.user, msg='Not the Usser')
        self.client.logout()
        data = {
            'text': 'test text1'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302, msg='is not redirect')
        self.assertEqual(Comment.objects.count(), 1, msg='created comment without author')
        self.client.force_login(self.user1)
        data = {
            'text': 'test_text2'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302, 'is not register')
        self.assertEqual(Comment.objects.count(), 2, msg='Comment is not Created')

    def test_comment_delete(self):
        self.client.force_login(self.user)
        self.book1 = Book.objects.create(title='test_title1')
        url = reverse('add-comment', kwargs=dict(slug=self.book1.slug))
        data = {
            'text': 'test text'
        }
        self.client.post(url, data)
        self.assertTrue(Comment.objects.exists(), msg='Not create comment')
        self.assertEqual(Comment.objects.count(), 1)
        comment1 = Comment.objects.first()
        self.assertEqual(comment1.author, self.user, msg='Not the Usser')
        self.book2 = Book.objects.create(title='test_title2')
        url = reverse('add-comment', kwargs=dict(slug=self.book2.slug))
        data = {
            'text': 'test text2'
        }
        self.client.post(url, data)
        comment2 = Comment.objects.last()
        self.assertEqual(Comment.objects.count(), 2)
        url = reverse('del-comment', kwargs=dict(slug=self.book1.slug, comment_id=comment1.id))
        self.client.get(url)
        self.assertEqual(Comment.objects.count(), 1)
        self.client.logout()
        url = reverse('del-comment', kwargs=dict(slug=self.book2.slug, comment_id=comment2.id))
        self.client.get(url)
        self.assertEqual(Comment.objects.count(), 1)
        self.client.force_login(self.user1)
        url = reverse('del-comment', kwargs=dict(slug=self.book2.slug, comment_id=comment2.id))
        self.client.get(url)
        self.assertEqual(Comment.objects.count(), 1)

    def test_update_comment(self):
        self.client.force_login(self.user)
        self.book1 = Book.objects.create(title='test_title1')
        url = reverse('add-comment', kwargs=dict(slug=self.book1.slug))
        data = {
            'text': 'test text'
        }
        self.client.post(url, data)
        comment1 = Comment.objects.first()
        self.book2 = Book.objects.create(title='test_title2')
        url = reverse('add-comment', kwargs=dict(slug=self.book2.slug))
        data = {
            'text': 'test text2'
        }
        self.client.post(url, data)
        comment2 = Comment.objects.last()
        data = {
             'text': 'test_text1_update'
        }
        url = reverse('update-comment', kwargs=dict(slug=self.book1.slug, comment_id=comment1.id))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        comment1.refresh_from_db()
        self.assertEqual(comment1.text, data['text'], msg='comment1 is not refreshed')
        self.assertEqual(comment1.author, self.user)
        self.client.logout()
        url = reverse('update-comment', kwargs=dict(slug=self.book2.slug, comment_id=comment2.id))
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        comment1.refresh_from_db()
        self.assertNotEqual(comment2.text, data['text'], msg='comment1 is not refreshed')
        self.assertEqual(comment1.author, self.user)
        self.client.force_login(self.user1)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        comment1.refresh_from_db()
        self.assertNotEqual(comment2.text, data['text'], msg='comment1 is not refreshed')

    def test_add_like_comment(self):
        self.client.force_login(self.user)
        self.book1 = Book.objects.create(title='test_title1')
        url = reverse('add-comment', kwargs=dict(slug=self.book1.slug))
        data = {
            'text': 'test text'
        }
        self.client.post(url, data)
        comment1 = Comment.objects.first()
        url = reverse("add-like", kwargs=dict(slug=self.book1.slug, comment_id=comment1.id))
        self.client.get(url)
        self.assertEqual(LikeCommentUser.objects.count(), 1)
        url = reverse("add-like", kwargs=dict(slug=self.book1.slug, comment_id=comment1.id))
        self.client.get(url)
        self.assertEqual(LikeCommentUser.objects.count(), 0)
        self.client.logout()
        url = reverse("add-like", kwargs=dict(slug=self.book1.slug, comment_id=comment1.id))
        self.client.get(url)
        self.assertEqual(LikeCommentUser.objects.count(), 0)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_login(self):
        url = reverse('login')
        data = {
            'username': 'Michail',
            'password': 'Michail27.03'
        }
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, msg='is not redirect')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302, msg='is not redirect')
        self.assertTrue(User.objects.exists(), msg='User is not enter')

    def test_logout(self):
        self.client.force_login(self.user)
        url = reverse('logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302, msg='is not redirect')
        self.assertTrue(User.objects.exists(), msg='User is not enter')

    def test_register(self):
        url = reverse('register')
        data = {
            'username': 'Michail',
            'password1': 'useruser',
            'password2': 'useruser'
        }
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, msg='is not redirect')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302, msg='is not redirect')
        self.assertTrue(User.objects.exists(), msg='User is not enter')
        self.client.logout()
        data = {
            'username': 'Michail',
            'password': 'useruser'
        }
        url = reverse('login')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302, msg='is not redirect')
        self.assertTrue(User.objects.exists(), msg='User is not enter')
        self.client.logout()
        data = {
            'username': 'Michail2345',
            'password1': 'useruser',
            'password2': 'user'
        }
        url = reverse('register')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.exists())

    def test_my_page(self):
        self.client.force_login(self.user)
        url = reverse('the-main-page')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'index.html')

    def test_PegeGenre(self):
        self.client.force_login(self.user)
        self.book1 = Book.objects.create(title='test_title1')
        self.book1.authors.add(self.user)
        self.book1.save()
        url = reverse('page-genre', kwargs=dict(genre=self.book1.genre))
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'page_books_genre.html')

    def test_BookDetail(self):
        self.client.force_login(self.user)
        self.book1 = Book.objects.create(title='test_title1', book_image='image')
        self.book1.authors.add(self.user)
        self.book1.save()
        url = reverse('book-detail', kwargs=dict(slug=self.book1.slug))
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'book_detail.html')




# coverage run --source="." manage.py test
# coverage html

