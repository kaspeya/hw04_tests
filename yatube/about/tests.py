from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class AboutURLTests(TestCase):
    def setUp(self):
        # Создаем неавторизованый клиент
        self.guest_client = Client()

    def test_about_author_url(self):
        """Проверка доступности адреса /about/author/."""
        """Проверка шаблона для адреса /about/author/."""
        response = self.guest_client.get('/about/author/')
        self.assertTemplateUsed(response, 'about/author.html')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_about_tech_url(self):
        """Проверка доступности адреса /about/tech/."""
        """Проверка шаблона для адреса /about/tech/."""
        response = self.guest_client.get('/about/tech/')
        self.assertTemplateUsed(response, 'about/tech.html')
        self.assertEqual(response.status_code, HTTPStatus.OK)


class AboutViewTests(TestCase):
    def setUp(self):
        # Создаем неавторизованый клиент
        self.guest_client = Client()

    def test_about_author_accessible_by_name(self):
        """URL, генерируемый при помощи имени about:author, доступен."""
        response = self.guest_client.get(reverse('about:author'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_about_author_uses_correct_template(self):
        """При запросе about:author применяется шаблон 'about/author.html'."""
        response = self.guest_client.get(reverse('about:author'))
        self.assertTemplateUsed(response, 'about/author.html')

    def test_about_tech_accessible_by_name(self):
        """URL, генерируемый при помощи имени about:tech, доступен."""
        response = self.guest_client.get(reverse('about:tech'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_about_tech_uses_correct_template(self):
        """При запросе к about:author применяется шаблон 'about/tech.html'."""
        response = self.guest_client.get(reverse('about:tech'))
        self.assertTemplateUsed(response, 'about/tech.html')
