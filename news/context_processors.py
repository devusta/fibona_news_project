from .models import News, Category, Comment
from django.db.models import Count
from hitcount.models import HitCount


def news_context(request):
    news_context = News.published.all().order_by('-publish_time')[:10]
    categories = Category.objects.all()
    popular_news_ids = HitCount.objects.filter(content_type__model='news') \
                                        .values('object_pk') \
                                        .annotate(hit_count=Count('hits')) \
                                        .order_by('-hit_count')[:4] \
                                        .values_list('object_pk', flat=True)
    popular_news = News.objects.filter(id__in=popular_news_ids)
    cat_urls = ['social_news', 'tech_news', 'sport_news', 'science_news', 'economic_news', 'world_news']
    category_urls = {}
    for category in reversed(categories):
        for cat_url in cat_urls:
            if str(category)[:4] == cat_url[:4]:
                category_urls[category] = cat_url

    all_comments = Comment.objects.filter(is_active=True).order_by('-created_time')[:5]

    context = {
        'news_context': news_context,
        'categories': categories,
        'popular_news': popular_news,
        'category_urls': category_urls,
        'all_comments': all_comments,
    }
    return context
