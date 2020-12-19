from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# from django.views.decorators.cache import cache_page

from .models import Post, Group, Follow, User
from .forms import PostForm, CommentForm


# @cache_page(20)
def index(request):
    post_list = Post.objects.select_related('group')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'index.html',
        {'page': page, 'paginator': paginator,}
    )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'group.html',
        {'group': group, 'page': page, 'paginator': paginator,}
    )


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    profile_post_list = profile.posts.all()
    posts_count = profile_post_list.count()
    paginator = Paginator(profile_post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            user=request.user, author=profile).count()
    else:
        following = False
    return render(
        request,
        'profile.html',
        {'profile': profile,
         'page': page,
         'paginator': paginator,
         'posts_count': posts_count,
         'following': following}
    )


def post_view(request, username, post_id):
    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author=profile)
    comments = post.comments.all()
    profile_post_list = profile.posts.all()
    posts_count = profile_post_list.count()
    form = CommentForm()
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            user=request.user, author=profile).count()
    else:
        following = False
    return render(
        request,
        'post.html',
        {'profile': profile,
         'posts_count': posts_count,
         'post': post,
         'comments': comments,
         'form': form,
         'following': following}
    )


@login_required
def add_comment(request, username, post_id):
    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author=profile)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('post_view', username=username, post_id=post_id)
    return render(request, 'post.html')


@login_required
def post_edit(request, username, post_id):
    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author=profile)
    if request.user == post.author:
        form = PostForm(request.POST or None,
                        files=request.FILES or None,
                        instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_view', username=username, post_id=post_id)
        return render(
            request,
            'post_edit.html',
            {'form': form,
             'username': username,
             'post': post}
        )
    return redirect('post_view', username=username, post_id=post_id)


@login_required
def new_post(request):
    form = PostForm(request.POST or None,
                    files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('index')
    return render(
        request,
        'new_post.html',
        {'form': form}
    )


@login_required
def follow_index(request):
    post_list = Post.objects.filter(
        author__following__user=request.user).all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'follow.html',
        {'page': page, 
         'paginator': paginator})


@login_required
def profile_follow(request, username):
    #Тот, на кого подписываются
    follow = get_object_or_404(User, username=username)
    #Тот, кто подписывается
    follower = User.objects.get(username=request.user.username)
    if follow == follower:
        return redirect('profile', username)
    favorite_object = Follow.objects.filter(
        user=follower, author=follow).count()
    if not favorite_object:
        #Тот, кто подписывается
        Follow.objects.create(user=follower, author=follow)
    return redirect('profile', username)


@login_required
def profile_unfollow(request, username):
    #Тот, от кого отписываются
    follow = get_object_or_404(User, username=username)
    #Тот, кто отписывается
    follower = User.objects.get(username=request.user.username)
    Follow.objects.filter(user=follower, author=follow).delete()
    return redirect('profile', username)


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500) 
