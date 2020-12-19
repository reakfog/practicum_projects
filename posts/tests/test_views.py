from django import forms
from django.urls import reverse
from posts.tests.base import PostBaseTestCase
from django.contrib.flatpages.models import FlatPage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache import cache 

from posts.models import Post, Follow, Comment


class ViewsTest(PostBaseTestCase):
    # Фикстуры
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        for case in range(2,14):
            Post.objects.get(id=case).delete()

        cls.new_post = Post.objects.get(id=1)
        img = (b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B')
        uploaded = SimpleUploadedFile(
            name='small.jpeg',
            content=img,
            content_type='image/jpeg')
        cls.new_post.image = uploaded

    # Проверка, какой шаблон будет вызван при обращении к view-функциям
    def test_pages_use_correct_templates(self) -> None:
        pages = ViewsTest.pages
        authorized_client_1 = ViewsTest.authorized_client_1
        for template, reverse_name in pages.items():
            with self.subTest(reverse_name=reverse_name):
                response = authorized_client_1.get(reverse_name)
                self.assertTemplateUsed(response, template)

    # Проверка, соответствует ли ожиданиям словарь context во всех шаблонах
    def test_pages_shows_correct_context(self) -> None:
        pages = ViewsTest.pages
        authorized_client_1 = ViewsTest.authorized_client_1
        for template, reverse_name in pages.items():
            with self.subTest():
                test_contexts = {
                    'profile': ViewsTest.user_1,
                    'group': ViewsTest.new_group,
                    'page': ViewsTest.new_post,
                    'post': ViewsTest.new_post,
                    'posts_count': Post.objects.all().count(),
                }
                response = authorized_client_1.get(reverse_name).context
                for context_key, context_value in test_contexts.items():
                    with self.subTest():
                        if context_key in response:
                            tested = response.get(context_key)
                            if context_key == 'page':
                                tested = tested[0]
                            else:
                                tested = tested
                            self.assertEqual(
                                tested,
                                context_value,
                                f'Неправильный context'
                                f'({context_key}) в {template}'
                            )

    # Проверка, соответствует ли ожиданиям словарь context
    # в шаблонах с формами
    def test_form_pages_show_correct_context(self) -> None:
        pages = ViewsTest.pages
        authorized_client_1 = ViewsTest.authorized_client_1
        pages_list = ['new_post.html', 'post_edit.html']
        for template in pages_list:
            response = authorized_client_1.get(pages[template])
            form_fields = {
                'group': forms.fields.ChoiceField,
                'text': forms.fields.CharField
            }
            for value, expected in form_fields.items():
                with self.subTest(value=value):
                    form = response.context.get('form')
                    form_field = form.fields.get(value)
                    self.assertIsInstance(
                        form_field,
                        expected,
                        f'Неправильный context'
                        f'({value}) в {template}'
                        )

    # Проверка, не появляется ли пост в ненужной группе
    def test_post_appear_correctly(self) -> None:
        authorized_client_1 = ViewsTest.authorized_client_1
        reverse_page = reverse(
            'group_posts',
            kwargs={'slug': ViewsTest.second_group.slug}
        )
        response = authorized_client_1.get(reverse_page)
        self.assertEqual(len(response.context['page']), 0)


class FollowAndCommentTest(PostBaseTestCase):
    def test_follow(self) -> None:
        authorized_client_1 = FollowAndCommentTest.authorized_client_1
        user_1 = FollowAndCommentTest.user_1
        user_2 = FollowAndCommentTest.user_2
        authorized_client_1.get(
            reverse('profile_follow', kwargs={'username': user_2.username})
        )
        following = Follow.objects.filter(user=user_1, author=user_2).count()
        self.assertEqual(following, 1)
        authorized_client_1.get(
            reverse('profile_unfollow', kwargs={'username': user_2.username})
        )
        following = Follow.objects.filter(user=user_1, author=user_2).count()
        self.assertEqual(following, 0)

    def test_follow_index(self) -> None:
        authorized_client_1 = FollowAndCommentTest.authorized_client_1
        user_1 = FollowAndCommentTest.user_1
        user_2 = FollowAndCommentTest.user_2
        Post.objects.create(text='Текст избранного автора',
                            author=user_2)
        authorized_client_1.get(
            reverse('profile_follow', kwargs={'username': user_2.username})
        )
        response = authorized_client_1.get(reverse('follow_index'))
        context = response.context.get('page')[0].text
        self.assertEqual(context, 'Текст избранного автора')


class FlatpagesViewsTest(PostBaseTestCase):
    # Проверка, соответствует ли ожиданиям словарь context в flatpages
    def test_flatpages_shows_correct_context(self) -> None:
        flatpages = FlatpagesViewsTest.flatpages
        guest_client = FlatpagesViewsTest.guest_client
        for template, url in flatpages.items():
            with self.subTest():
                flatpage = FlatPage.objects.create(
                    url=url,
                    title=f'Title for {template}',
                    content=f'Content for {template}')
                flatpage.sites.add(1)
                flatpage.save()
                response = guest_client.get(url).context.get('flatpage')
                self.assertEqual(
                    response,
                    FlatPage.objects.get(url=url),
                    f'Неправильный context в {template}'
                )


class PaginatorViewsTest(PostBaseTestCase):
    def test_pages_have_expected_count_of_records(self) -> None:
        pages = PaginatorViewsTest.pages
        authorized_client_1 = PaginatorViewsTest.authorized_client_1
        pages_with_records = {
            'index': pages['index.html'],
            'group_posts': pages['group.html']
        }
        for page, reverse_name in pages_with_records.items():
            response = authorized_client_1.get(reverse_name)
            self.assertEqual(
                len(response.context.get('page').object_list),
                10,
                f'На первой странице {page} неправильное кол-во записей'
            )
            response = authorized_client_1.get(reverse_name + '?page=2')
            self.assertEqual(
                len(response.context.get('page').object_list),
                3,
                f'На второй странице {page} неправильное кол-во записей'
            )


class CacheTest(PostBaseTestCase):
    def test_home_page_cahe(self) -> None:
        pages = CacheTest.pages
        guest_client = CacheTest.guest_client
        response = guest_client.get(pages['index.html'])
        content = response.content
        Post.objects.all().delete()
        response = guest_client.get(pages['index.html'])
        self.assertEqual(
            content,
            response.content,
            'Кеширование неисправно')
        cache.clear()
        response = guest_client.get(pages['index.html'])
        self.assertNotEqual(
            content,
            response.content,
            'Кеширование неисправно')
