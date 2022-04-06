from django.test import TestCase

from ..models import Group, Post, User
from ..tests import constants


class PostModelTest(TestCase):
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
            group=PostModelTest.group,
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        group = PostModelTest.group
        post = PostModelTest.post
        expected_object_name = group.title
        expected_object_text = post.text[:15]
        self.assertEqual(expected_object_name, str(group))
        self.assertEqual(expected_object_text, str(post))

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        group = PostModelTest.group
        post = PostModelTest.post
        field_verbose_group = {
            'title': 'Имя',
            'slug': 'Адрес',
            'description': 'Описание',
        }
        field_verbose_post = {
            'text': 'Текст',
            'author': 'Автор',
        }
        for field, expected_value in field_verbose_group.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).verbose_name, expected_value)

        for field, expected_value in field_verbose_post.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value)

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        post = PostModelTest.post
        field_help_text_post = {
            'text': 'Введите текст поста',
            'group': 'Группа, к которой будет относиться пост',
        }
        for field, expected_value in field_help_text_post.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value)
