from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User
from ..tests import constants


class PostsFormsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=constants.USERNAME)
        cls.not_author_client = User.objects.create_user(username='NoName')
        cls.group = Group.objects.create(
            title=constants.GROUP_TITLE,
            slug=constants.GROUP_SLUG,
            description=constants.GROUP_DESCRIPTION,
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=constants.POST_TEXT,
            group=PostsFormsTests.group,
        )
        cls.group_2 = Group.objects.create(
            title=f'{constants.GROUP_TITLE}_2',
            slug=f'{constants.GROUP_SLUG}_2',
            description=f'{constants.GROUP_DESCRIPTION}_2',
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.not_author_client = Client()

    def test_create_post(self):
        post_count = Post.objects.count()
        form_data = {
            'text': 'test_text',
            'group': self.group.id
        }
        response = self.authorized_client.post(reverse(
            'posts:post_create'),
            data=form_data,
            follow=True
        )
        post = Post.objects.first()
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': self.user}))
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.group.id, self.group.id)
        self.assertEqual(post.author, self.user)

    def test_edit_post(self):
        post_count = Post.objects.count()
        form_data = {
            'text': 'test_text_1',
            'group': self.group_2.id
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk}),
            data=form_data,
            follow=False
        )
        post = Post.objects.get(pk=self.post.pk)
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': self.post.pk}))
        self.assertEqual(Post.objects.count(), post_count)
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.group.id, self.group_2.id)

    def test_not_author_trys_edit_post(self):
        form_data = {
            'text': 'test_text_2',
            'group': self.group.id
        }
        self.authorized_client.logout()
        response = self.not_author_client.post(reverse(
            'posts:post_edit', kwargs={'post_id': self.post.pk}),
            data=form_data,
            follow=True
        )
        redirect_url = '{}?next={}'.format(
            reverse('users:login'),
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk})
        )
        self.assertRedirects(response, redirect_url)
