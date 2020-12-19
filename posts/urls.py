from django.urls import path
from . import views


urlpatterns = [
    # Главная страница
    path('',
        views.index,
        name='index'),
    # Группы
    path('group/<slug:slug>/',
        views.group_posts,
        name='group_posts'),
    # Создание новой записи
    path('new/',
        views.new_post,
        name='new_post'),
    # Посты избранных авторов
    path('follow/',
        views.follow_index,
        name='follow_index'),
    # Подписаться
    path('<str:username>/follow/',
        views.profile_follow,
        name='profile_follow'),
    # Отписаться
    path('<str:username>/unfollow/',
        views.profile_unfollow,
        name='profile_unfollow'),
    # Профайл пользователя
    path('<str:username>/',
        views.profile,
        name='profile'),
    # Просмотр записи
    path('<str:username>/<int:post_id>/',
        views.post_view,
        name='post_view'),
    # Комментирование записи
    path('<str:username>/<int:post_id>/comment',
        views.add_comment,
        name='add_comment'),
    # Редактирование записи
    path('<str:username>/<int:post_id>/edit/',
        views.post_edit,
        name='post_edit'),
    # Страницы ошибок
    path('404',
        views.page_not_found,
        name='page_not_found'),
    path('500',
        views.server_error,
        name='server_error'),
]
