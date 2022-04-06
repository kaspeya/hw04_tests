from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Contact

User = get_user_model()


class ContactURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.contact = Contact.objects.create(
            name='Имя',
            email='Почта',
            subject='Тема письма',
            body='Сообщение',
        )

        cls.users_public_url_names = (
            ('/auth/signup/', 'users/signup.html'),
            ('/auth/login/', 'users/login.html'),
            ('/auth/password_reset/', 'users/password_reset_form.html'),
            ('/auth/password_reset/done/', 'users/password_reset_done.html'),
            ('/auth/reset/<uidb64>/<token>/',
             'users/password_reset_confirm.html'),
            ('/auth/reset/done/', 'users/password_reset_complete.html'),
            ('/auth/contact/', 'users/contact.html'),
            ('/auth/thankyou/', 'users/thankyou.html'),
        )
        cls.authorized_client_url_names = (
            ('/auth/logout/', 'users/logged_out.html'),
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='auth')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_url_users(self):
        """URL-адрес использует соответствующий шаблон."""
        for url, template in self.users_public_url_names:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)
                self.assertEqual(response.status_code, HTTPStatus.OK)
        for url, template in self.authorized_client_url_names:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_url_returns_404_error(self):
        """Запрос к несуществующей странице вернёт ошибку 404."""
        response = self.guest_client.get('/auth/unexisting_page/')
        self.assertEqual(response.status_code, 404)
