from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class UserFormsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='vanya', password='password')

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()

    def test_create_user(self):
        form_data = {
            'username': self.user.username,
            'password': self.user.password
        }
        self.guest_client.post(reverse(
            'users:signup'), data=form_data, follow=True
        )
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)
