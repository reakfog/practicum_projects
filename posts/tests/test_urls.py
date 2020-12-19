from django.contrib.flatpages.models import FlatPage
from posts.tests.base import PostBaseTestCase


class URLTests(PostBaseTestCase):
    # Проверка работы страниц для неавторизованных пользователей
    def test_pages_for_guest_clients(self) -> None:
        pages = URLTests.pages
        guest_client = URLTests.guest_client
        for page_name, url in pages.items():
            with self.subTest():
                if page_name in ['index.html',
                                 'group.html',
                                 'profile.html',
                                 'post.html']:
                    response = guest_client.get(url)
                    self.assertEqual(
                        response.status_code,
                        200,
                        f'Шаблон - {page_name}, '
                        f'URL - {url}, '
                        f'Фактический статус - {response.status_code}, '
                        'Ожидаемый статус - 200.')
                else:
                    response = guest_client.get(url)
                    self.assertNotEqual(
                        response.status_code,
                        200,
                        f'Шаблон - {page_name}, '
                        f'URL - {url}, '
                        f'Фактический статус - {response.status_code}, '
                        'Ожидаемый статус - не 200.')
    
    # Проверка работы страниц для авторизованных пользователей
    def test_pages_for_authorized_client(self) -> None:
        pages = URLTests.pages
        authorized_client_1 = URLTests.authorized_client_1
        authorized_client_2 = URLTests.authorized_client_2
        for page_name, url in pages.items():
            with self.subTest():
                response = authorized_client_1.get(url)
                self.assertEqual(
                    response.status_code,
                    200,
                    f'Шаблон - {page_name}, '
                    f'URL - {url}, '
                    f'Фактический статус - {response.status_code}, '
                     'Ожидаемый статус - 200.')
        response = authorized_client_2.get(pages['post_edit.html'])
        self.assertNotEqual(
            response.status_code,
            200,
            'Шаблон - post_edit.html, '
            'URL - /test_user_1/1/edit/, '
            f'Фактический статус - {response.status_code}, '
             'Ожидаемый статус - не 200.'
        )
    
    # Проверка вызоваемых шаблонов для неавторизованных пользователей
    def test_templates_for_guest_clients(self) -> None:
        pages = URLTests.pages
        guest_client = URLTests.guest_client
        for page_name, url in pages.items():
            with self.subTest():
                if page_name in ['index.html',
                                 'group.html',
                                 'profile.html',
                                 'post.html']:
                    response = guest_client.get(url)
                    self.assertTemplateUsed(
                        response,
                        page_name,
                        f'Шаблон {page_name} не используется для URL {url}'
                         'а должен'
                    )
                else:
                    response = guest_client.get(url)
                    self.assertTemplateNotUsed(
                        response,
                        page_name,
                        f'Шаблон {page_name} используется для URL {url}, '
                         'а не должен'
                    )

    # Проверка вызоваемых шаблонов для авторизованных пользователей
    def test_templates_for_authorized_client(self) -> None:
        pages = URLTests.pages
        authorized_client_1 = URLTests.authorized_client_1
        for page_name, url in pages.items():
            with self.subTest():
                response = authorized_client_1.get(url)
                self.assertTemplateUsed(
                    response,
                    page_name,
                    f'Шаблон {page_name} не используется для URL {url}, '
                     'а должен'
                )

    # Проверка работы редиректа со страницы редактирования поста
    # для тех у кого нет прав доступа
    def test_redirect_from_edit_post_for_client_with_no_access(self) -> None:
        pages = URLTests.pages
        authorized_client_2 = URLTests.authorized_client_2
        response = authorized_client_2.get(pages['post_edit.html'])
        self.assertRedirects(response, pages['post.html'])


class StaticURLTests(PostBaseTestCase):
    # Проверка работы страниц
    def test_pages_for_guest_clients(self) -> None:
        flatpages = StaticURLTests.flatpages
        guest_client = StaticURLTests.guest_client
        for page_name, url in flatpages.items():
            with self.subTest():
                flatpage = FlatPage.objects.create(url=f'{url}')
                flatpage.sites.add(1)
                flatpage.save()
                response = guest_client.get(url)
                self.assertEqual(
                    response.status_code,
                    200,
                    f'Шаблон - {page_name}, '
                    f'URL - {url}, '
                    f'Фактический статус - {response.status_code}, '
                    'Ожидаемый статус - 200.')

class PageErrorURLTests(PostBaseTestCase):
    # Проверка возврата сервером кода 404
    def test_server_returns_code_404_if_page_not_found(self) -> None:
        errorpages = PageErrorURLTests.errorpages
        guest_client = PageErrorURLTests.guest_client
        response = guest_client.get('/test_page/')
        self.assertEqual(
            response.status_code,
            404,
            f'Фактический статус - {response.status_code}, '
             'Ожидаемый статус - 404'
        )
