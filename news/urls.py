from django.urls import path
from .views import (
    NewsListView,
    NewsDetailView,
    HomePageView,
    ContactView,
    SocialNewsView,
    TechnologyNewsView,
    SportNewsView,
    ScienceNewsView,
    EconomicNewsView,
    WorldNewsView,
    NewsCreateView,
    NewsUpdateView,
    NewsDeleteView,
    SearchResultsView,
    AboutView,
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('news/<slug:slug>/', NewsDetailView.as_view(), name='news_detail'),
    path('social/', SocialNewsView.as_view(), name='social_news'),
    path('technology/', TechnologyNewsView.as_view(), name='tech_news'),
    path('sport/', SportNewsView.as_view(), name='sport_news'),
    path('economical/', EconomicNewsView.as_view(), name='economic_news'),
    path('science/', ScienceNewsView.as_view(), name='science_news'),
    path('world/', WorldNewsView.as_view(), name='world_news'),
    path('news/', NewsListView.as_view(), name='news_list'),
    path('create/', NewsCreateView.as_view(), name='news_create'),
    path('<slug>/edit/', NewsUpdateView.as_view(), name='news_edit'),
    path('<slug>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('searchresults/', SearchResultsView.as_view(), name='search_results'),
    path('about/', AboutView.as_view(), name='about'),
]

