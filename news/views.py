from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormMixin
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountDetailView, HitCountMixin
from .forms import ContactForm, CommentForm
from .models import News, Category
from config.custom_permissions import CustomUserPassesTestMixin
from django.views.generic import (
    ListView,
    TemplateView,
    UpdateView,
    CreateView,
    DeleteView,
)


class HomePageView(TemplateView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_list'] = News.published.all().order_by('-publish_time')
        context['social_news'] = News.published.all().filter(category__name='social').order_by('-publish_time')[:5]
        context['tech_news'] = News.published.filter(category__name='technology').order_by('-publish_time')[:5]
        context['sport_news'] = News.published.all().filter(category__name='sport').order_by('-publish_time')[:5]
        context['science_news'] = News.published.all().filter(category__name='science').order_by('-publish_time')[:5]
        context['economic_news'] = News.published.all().filter(category__name='economical').order_by('-publish_time')[:5]
        context['categories'] = Category.objects.all().order_by('-id')
        return context


class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'

    def get_queryset(self):
        return self.model.published.all().order_by('-publish_time')


class NewsDetailView(FormMixin, HitCountDetailView):    # classga asoslangan NewsDetailView
    model = News
    count_hit = True
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('news_detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(is_active=True)
        if 'comment_form' not in context:
            context['comment_form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if request.user.is_authenticated:
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.news = self.object
                new_comment.author = self.request.user
                new_comment.save()
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            return redirect('login')


def news_detail_view(request, news):    # funksiyaga asoslangan news_detail_view
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    hit_count = get_hitcount_model().objects.get_for_object(news)
    context = {}
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    comments = news.comments.filter(is_active=True)
    new_comment = None

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            news_comment = comment_form.save(commit=False)
            news_comment.news = news
            news_comment.author = request.user
            news_comment.save()
            return redirect(news_detail_view, news=news.slug)
    else:
        comment_form = CommentForm()

    context = {
        'news': news,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
    }
    return render(request, 'news/news_detail.html', context)


class SocialNewsView(ListView):
    model = News
    template_name = 'news/social_news.html'
    context_object_name = 'social_news'

    def get_queryset(self):
        return self.model.published.all().filter(category__name='social').order_by('-publish_time')


class TechnologyNewsView(ListView):
    model = News
    template_name = 'news/tech_news.html'
    context_object_name = 'tech_news'

    def get_queryset(self):
        return self.model.published.all().filter(category__name='technology').order_by('-publish_time')


class SportNewsView(ListView):
    model = News
    template_name = 'news/sport_news.html'
    context_object_name = 'sport_news'

    def get_queryset(self):
        return self.model.published.all().filter(category__name='sport').order_by('-publish_time')


class ScienceNewsView(ListView):
    model = News
    template_name = 'news/science_news.html'
    context_object_name = 'science_news'

    def get_queryset(self):
        return self.model.published.all().filter(category__name='science').order_by('-publish_time')


class EconomicNewsView(ListView):
    model = News
    template_name = 'news/economic_news.html'
    context_object_name = 'economic_news'

    def get_queryset(self):
        return self.model.published.all().filter(category__name='economical').order_by('-publish_time')


class WorldNewsView(ListView):
    model = News
    template_name = 'news/world_news.html'
    context_object_name = 'world_news'

    def get_queryset(self):
        return self.model.published.all().filter(category__name='world').order_by('-publish_time')


class ContactView(TemplateView):
    template_name = 'news/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            'form': form
        }
        return render(request, 'news/contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse("<h2>Thank you for contacting us!</h2>")
        context = {
            'form': form
        }
        return render(request, 'news/contact.html', context)


# def contact_page_view(request):
#     form = ContactForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         form.save()
#         return HttpResponse('<h2>Your message has been sent</h2>')
#     context = {
#         "form": form
#     }
#
#     return render(request, 'news/contact.html', context)


class NewsUpdateView(CustomUserPassesTestMixin, UpdateView):
    model = News
    fields = ['title', 'body', 'category', 'image', 'status']
    template_name = 'crud/news_edit.html'


class NewsDeleteView(CustomUserPassesTestMixin, DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home')


class NewsCreateView(CustomUserPassesTestMixin, CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ['title', 'slug', 'body', 'category', 'image', 'status']


class SearchResultsView(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'news_list'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return News.objects.filter(
                Q(title__icontains=query) | Q(body__icontains=query)
            )