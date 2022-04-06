from http import HTTPStatus

from django.test import Client, TestCase

from ..models import Group, Post, User
from ..tests import constants


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=constants.USERNAME)
        cls.group = Group.objects.create(
            title=constants.GROUP_TITLE,
            slug=constants.GROUP_SLUG,
            description=constants.GROUP_DESCRIPTION,
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=constants.POST_TEXT,
            group=PostURLTests.group,
        )
        cls.public_url_names = (
            ('/', 'posts/index.html'),
            (f'/group/{cls.group.slug}/', 'posts/group_list.html'),
            (f'/profile/{cls.user.username}/', 'posts/profile.html'),
            (f'/posts/{cls.post.id}/', 'posts/post_detail.html'),
        )
        cls.authorized_client_url_names = (
            ('/create/', 'posts/post_create.html'),
            (f'/posts/{cls.post.pk}/edit/', 'posts/post_create.html'),
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_url_uses_correct_template_and_exists_at_desired_location(self):
        """URL-адрес использует соответствующий шаблон."""
        for url, template in self.public_url_names:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)
                self.assertEqual(response.status_code, HTTPStatus.OK)
        for url, template in self.authorized_client_url_names:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_create_url_redirects_guest_client_on_user_login(self):
        """Страница /create/ перенаправит неавторизованного пользователя
        на страницу /login/."""
        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_edit_url_redirects_not_author_on_post_detail(self):
        """Страница /posts/post_id/edit/ перенаправит не автора
        на страницу /posts/post_id/."""
        if self.post.author != self.user:
            response = self.authorized_client.post(
                f'/posts/{self.post.pk}/edit/', follow=True)
            self.assertRedirects(
                response, f'/posts/{self.post.pk}/')
            self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_url_returns_404_error(self):
        """Запрос к несуществующей странице вернёт ошибку 404."""
        response = self.guest_client.get('/unexisting_page/')
        self.assertTemplateUsed(response, '404.html')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
