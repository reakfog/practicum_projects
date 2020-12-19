from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Post(models.Model):
    text = models.TextField(
                verbose_name='Текст публикации',
                help_text='Опишите Ваши мысли')
    pub_date = models.DateTimeField(
                'date published',
                auto_now_add=True,
                db_index=True)
    author = models.ForeignKey(
                User,
                on_delete=models.CASCADE,
                related_name='posts',
                verbose_name='Автор')
    group = models.ForeignKey(
                'Group',
                on_delete=models.SET_NULL,
                blank=True,
                null=True,
                related_name='posts',
                verbose_name='Сообщество',
                help_text='Выберите сообщество в выпадающем '
                          'списке, или оставте это поле пустым')
    image = models.ImageField(
                upload_to='posts/',
                blank=True,
                null=True)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-pub_date',)
    
    def __str__(self):
        return self.text[:15]


class Group(models.Model):
    title = models.CharField(
                max_length=200,
                verbose_name="Название сообщества")
    slug = models.SlugField(
                unique=True,
                verbose_name="Адрес")
    description = models.TextField(
                verbose_name="Краткое описание")

    class Meta:
        verbose_name = 'Сообщество'
        verbose_name_plural = 'Сообщества'
        ordering = ('-slug',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField(
                verbose_name='Текст комментария',
                help_text='Опишите Ваши мысли')
    created = models.DateTimeField(
                'date published',
                auto_now_add=True)
    post = models.ForeignKey(
                Post,
                null=True,
                on_delete=models.CASCADE,
                related_name='comments',
                verbose_name='Пост')
    author =  models.ForeignKey(
                User,
                null=True,
                on_delete=models.CASCADE,
                related_name='comments',
                verbose_name='Автор')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created',)

    def __str__(self):
        return self.text


class Follow(models.Model):
    user = models.ForeignKey(
                User,
                null=True,
                on_delete=models.CASCADE,
                related_name='follower',
                verbose_name='Подписчик')
    author = models.ForeignKey(
                User,
                null=True,
                on_delete=models.CASCADE,
                related_name='following',
                verbose_name='Автор')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-author',)
    
    def __str__(self):
        return f'{self.user} подписан на {self.author}'
