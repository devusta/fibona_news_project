from .models import News, Category


def news_context(request):
    news_context = News.published.all().order_by('-publish_time')[:10]
    categories = Category.objects.all()
    context = {
        'news_context': news_context,
        'categories': categories,
    }
    return context
