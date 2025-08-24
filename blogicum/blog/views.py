from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post

POSTS_ON_INDEX = 5


def _base_posts_qs():
    """Базовый queryset опубликованных постов с нужными связями/фильтрами."""
    return (
        Post.objects.select_related(
            'author',
            'category',
            'location',
        ).filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True,
        )
    )


def index(request):
    """Главная страница: последние 5 опубликованных постов."""
    qs = _base_posts_qs()[:POSTS_ON_INDEX]
    return render(
        request,
        'blog/index.html',
        {'post_list': qs},
    )


def category_posts(request, slug):
    """
    Страница категории.

    Показываем посты только если сама категория опубликована.
    Иначе возвращаем 404.
    """
    category = get_object_or_404(
        Category,
        slug=slug,
        is_published=True,
    )
    qs = _base_posts_qs().filter(
        category=category,
    )
    return render(
        request,
        'blog/category.html',
        {
            'category': category,
            'post_list': qs,
        },
    )


def post_detail(request, pk):
    """
    Детальная страница поста.

    404, если пост снят с публикации, дата в будущем
    или категория снята с публикации.
    """
    post = get_object_or_404(
        _base_posts_qs(),
        pk=pk,
    )
    return render(
        request,
        'blog/detail.html',
        {'post': post},
    )
