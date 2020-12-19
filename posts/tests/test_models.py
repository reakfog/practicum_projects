from posts.tests.base import PostBaseTestCase


class PostsModelsTest(PostBaseTestCase):
    # Проверка наличия verbose_name в модели Post (поля text, group)
    def test_verbose_name(self) -> None:
        new_post = PostsModelsTest.new_post
        verbose_names = {
            'text': 'Текст публикации',
            'group': 'Сообщество',
        }
        for field, expected in verbose_names.items():
            with self.subTest(value=field):
                self.assertEqual(
                    new_post._meta.get_field(field).verbose_name,
                    expected,
                    f'Параметр "verbose_name" не прописан в поле {field}')

    # Проверка наличия help_text в модели Post (поля text, group)
    def test_help_text(self) -> None:
        new_post = PostsModelsTest.new_post
        help_texts = {
            'text': 'Опишите Ваши мысли',
            'group': 'Выберите сообщество в выпадающем '
                     'списке, или оставте это поле пустым',
        }
        for field, expected in help_texts.items():
            with self.subTest(value=field):
                self.assertEqual(
                    new_post._meta.get_field(field).help_text,
                    expected,
                    f'Параметр "help_text" не прописан в поле {field}')

    # Проверка работы метода __str__ в моделях Post и Group
    def test_str_method(self) -> None:
        new_post = PostsModelsTest.new_post
        new_group = PostsModelsTest.new_group
        expectations = {
            new_post: '(№0) Текст данн',
            new_group: 'Lord of The Rings',
        }
        for model_obj, expected in expectations.items():
            with self.subTest():
                self.assertEqual(
                    str(model_obj),
                    expected,
                    f'Метод __str__ не работает в модели {type(model_obj)}')
