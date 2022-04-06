import time

from django import forms
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User
from ..tests import constants


class PostsURLTests(TestCase):
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
            group=PostsURLTests.group,
        )
        cls.group_1 = Group.objects.create(
            title=f'{constants.GROUP_TITLE}_1',
            slug=f'{constants.GROUP_SLUG}_1',
            description=f'{constants.GROUP_DESCRIPTION}_1',
        )
        cls.post_1 = Post.objects.create(
            text=f'{constants.POST_TEXT}_1',
            author=cls.user,
            group=cls.group_1,
        )
        test_post_count = 13
        for post_num in range(test_post_count):
            time.sleep(0.2)
            cls.post = Post.objects.create(
                author=cls.user,
                text='Тестовый пост %s' % post_num,
                group=cls.group,
            )
        cls.INDEX = ('posts/index.html', reverse('posts:index'))
        cls.GROUP_LIST = ('posts/group_list.html', reverse(
            'posts:group_list', kwargs={'slug': cls.group.slug}))
        cls.PROFILE = ('posts/profile.html', reverse(
            'posts:profile', kwargs={'username': cls.user.username}))
        cls.POST_DETAIL = ('posts/post_detail.html', reverse(
            'posts:post_detail', kwargs={'post_id': cls.post.pk}))
        cls.POST_CREATE = ('posts/post_create.html', reverse(
            'posts:post_create'))
        cls.POST_EDIT = ('posts/post_create.html', reverse(
            'posts:post_edit', kwargs={'post_id': cls.post.pk}))

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_reverse_names = (
            self.INDEX,
            self.GROUP_LIST,
            self.PROFILE,
            self.POST_DETAIL,
            self.POST_CREATE,
            self.POST_EDIT,
        )
        for template, reverse_name in templates_reverse_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(self.INDEX[1])
        post_object = response.context['page_obj'][0]
        self.assertEqual(post_object.text, self.post.text)
        self.assertEqual(post_object.group, self.post.group)
        self.assertEqual(post_object.author, self.post.author)
        self.assertEqual(len(response.context['page_obj']), 10)
        response = self.authorized_client.get(self.INDEX[1] + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 5)

    def test_group_posts_show_correct_context(self):
        """Шаблон Group сформирован с правильным контекстом."""
        response = self.authorized_client.get(self.GROUP_LIST[1])
        post_object = response.context['group']
        self.assertEqual(post_object.title, self.group.title)
        self.assertEqual(post_object.slug, self.group.slug)
        self.assertEqual(post_object.description, self.group.description)
        self.assertEqual(len(response.context['page_obj']), 10)
        response = self.authorized_client.get(reverse(
            'posts:group_list', kwargs={'slug': self.group.slug}) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 4)

    def test_profile_show_correct_context(self):
        """Шаблоны Profile сформированы с правильным контекстом."""
        response = self.authorized_client.get(self.PROFILE[1])
        self.assertEqual(len(response.context['page_obj']), 10)
        post_object = response.context['page_obj'][0]
        self.assertEqual(post_object.text, self.post.text)
        self.assertEqual(post_object.group, self.post.group)
        self.assertEqual(post_object.author, self.post.author)
        self.assertEqual(len(response.context['page_obj']), 10)
        response = self.authorized_client.get(self.PROFILE[1] + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 5)

    def test_post_detail_show_correct_context(self):
        """Шаблон Post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(self.POST_DETAIL[1])
        self.assertEqual(response.context['post'], self.post)
        self.assertTrue(Post.objects.filter(id=self.post.pk).exists())

    def test_create_show_correct_context(self):
        """Шаблон Post_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(self.POST_CREATE[1])
        form_fields = {'text': forms.CharField,
                       'group': forms.ModelChoiceField}
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
        post_object = response.context
        self.assertIn('form', post_object)

    def test_post_edit_page_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.authorized_client.post(self.POST_EDIT[1])
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
        post_object = response.context
        self.assertIn('form', post_object)
        self.assertIn('is_edit', post_object)

    def test_new_post_with_group(self):
        self.assertEqual(self.post_1.group, self.group_1)
        self.assertEqual(self.post_1.id, self.group_1.id)
        self.assertEqual(self.post_1.author, self.user)
        self.assertTrue(Post.objects.filter(id=self.post_1.pk).exists())
