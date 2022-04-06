from django.test import Client, TestCase
from django.urls import reverse


class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.templates_reverse_names = (
            ('users/signup.html', reverse('users:signup')),
            ('users/login.html', reverse('users:login')),
            ('users/password_reset_form.html', reverse(
                'users:password_reset')),
            ('users/password_reset_done.html', reverse(
                'users:password_reset_done')),
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        for template, reverse_name in self.templates_reverse_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
