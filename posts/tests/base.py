import shutil
import tempfile
from django.conf import settings
from django.urls import reverse
from django.test import Client, TestCase
from django.contrib.auth import get_user_model

from posts.forms import PostForm
from posts.models import Post, Group


class PostBaseTestCase(TestCase):
    # Фикстуры
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        # Создаём картинку и временную папку для медиа-файлов
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        # Создаём записи в базе: авторов, посты и группы:
        User = get_user_model()
        # Пользователь №1
        User.objects.create(
            username='test_user_1',
            email='test_user_1@gmail.com',
            password='Test12345')
        # Пользователь №2
        User.objects.create(
            username='test_user_2',
            email='test_user_2@gmail.com',
            password='Test12345')
        # Группа №1
        Group.objects.create(
            title='Lord of The Rings',
            slug='lotr',
            description='Описание группы')
        # Группа №2
        Group.objects.create(
            title='Star Wars',
            slug='sw',
            description='Описание группы')
        # Посты
        for case in range(0,13):
            Post.objects.create(
                text=f'(№{case}) Текст данного поста',
                author=User.objects.get(username='test_user_1'),
                group=Group.objects.get(slug='lotr'))
        # Создаем клиент:
        # Неавторизованный
        cls.guest_client = Client()
        # Авторизованный №1
        cls.user_1 = User.objects.get(username='test_user_1')
        cls.authorized_client_1 = Client()
        cls.authorized_client_1.force_login(cls.user_1)
        # Авторизованный №2
        cls.user_2 = User.objects.get(username='test_user_2')
        cls.authorized_client_2 = Client()
        cls.authorized_client_2.force_login(cls.user_2)
        # Создаем форму
        cls.form = PostForm()
        # Передаём в переменные данные, которые будем использовать
        cls.new_post = Post.objects.get(id=1)
        cls.new_group = Group.objects.get(slug='lotr')
        cls.second_group = Group.objects.get(slug='sw')
        cls.pages = {
            'index.html': reverse('index'),
            'group.html': reverse(
                'group_posts',
                kwargs={'slug': cls.new_group.slug}),
            'new_post.html': reverse('new_post'),
            'profile.html': reverse(
                'profile',
                kwargs={'username': cls.user_1.username}),
            'post.html': reverse(
                'post_view',
                kwargs={'username': cls.user_1.username,
                        'post_id': cls.new_post.id}),
            'post_edit.html': reverse(
                'post_edit',
                kwargs={'username': cls.user_1.username,
                        'post_id': cls.new_post.id}),
        }
        cls.flatpages = {
            'about-author.html': reverse('author'),
            'about-spec.html': reverse('spec'),
        }
        cls.errorpages = {
            404: reverse('page_not_found'),
            500: reverse('server_error'),
        }

    @classmethod
    # Удаляем временную папку для медиа-файлов
    def tearDownClass(cls) -> None:
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()