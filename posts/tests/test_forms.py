from posts.tests.base import PostBaseTestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from posts.models import Post


class FormsTest(PostBaseTestCase):
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
        cls.uploaded = SimpleUploadedFile(
            name='small.jpeg',
            content=img,
            content_type='image/jpeg')


    # Проверка, создаётся ли новый пост при отправке формы
    def test_create_new_post(self) -> None:
        authorized_client = FormsTest.authorized_client_1
        pages = FormsTest.pages
        posts_count = Post.objects.count()
        form_data = {
            'group': FormsTest.new_group.id,
            'text': 'Тестовый текст',
            'image': FormsTest.uploaded
        }
        response = authorized_client.post(
            pages['new_post.html'],
            data=form_data,
            follow=True
        )
        # Проверяем, сработал ли редирект
        self.assertRedirects(response, pages['index.html'])
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Post.objects.count(), posts_count+1)

    # Проверка, редактируется ли пост при отправке формы
    def test_edit_post(self) -> None:
        authorized_client = FormsTest.authorized_client_1
        pages = FormsTest.pages
        posts_count = Post.objects.count()
        form_data = {
            'group': FormsTest.new_group.id,
            'text': 'Изменённый текст'
        }
        response = authorized_client.post(
            pages['post_edit.html'],
            data=form_data,
            follow=True
        )
        # Проверяем, сработал ли редирект
        self.assertRedirects(response, pages['post.html'])
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Post.objects.count(), posts_count)
        # Проверяем, отредактирован ли конкретный пост
        self.assertEqual(Post.objects.get(id=1).text, 'Изменённый текст')

        