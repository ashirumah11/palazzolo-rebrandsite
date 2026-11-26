from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from .models import NewsArticle
from .serializers import NewsArticleSerializer


def news_list_view(request):
    """
    Public News & Stories feed with search, category filtering and pagination.
    """
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    queryset = NewsArticle.objects.filter(is_published=True).select_related()

    if query:
        queryset = queryset.filter(
            title__icontains=query
        ) | queryset.filter(
            summary__icontains=query
        ) | queryset.filter(
            content__icontains=query
        )
    if category:
        queryset = queryset.filter(category=category)

    paginator = Paginator(queryset, 9)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'query': query,
        'category': category,
        'page_obj': page_obj,
        'articles': page_obj.object_list,
    }
    return render(request, 'news/news_list.html', context)


def news_detail_view(request, slug):
    """
    Public news article detail page with related articles and social links.
    """
    article = get_object_or_404(NewsArticle, slug=slug, is_published=True)
    related = (
        NewsArticle.objects.filter(is_published=True)
        .exclude(pk=article.pk)
        .order_by('-published_at')[:4]
    )
    context = {
        'article': article,
        'related_articles': related,
    }
    return render(request, 'news/news_detail.html', context)


class NewsArticleListCreateAPIView(generics.ListCreateAPIView):
    """
    Publicly lists all published news articles.
    Creation requires auth unless you specifically want public creation.
    """
    queryset = NewsArticle.objects.filter(is_published=True)
    serializer_class = NewsArticleSerializer
    permission_classes = [AllowAny]


class NewsArticleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Allows public GET access to individual news articles,
    while restricting PUT, PATCH, and DELETE to authenticated users.
    """
    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]