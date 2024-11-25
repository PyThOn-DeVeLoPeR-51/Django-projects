from django.urls import path
from .views import NewsListView, HomePageView, ContactPageView, LocalNewsView, \
    ForeignNewsView, TechnoNewsView, SportNewsView, UpdateNewsView, DeleteNewsView, CreateNewsView, admin_page_view, \
    news_detail, SearchResaltView

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('all-news/', NewsListView.as_view(), name='news_list'),
    path('news/create/', CreateNewsView.as_view(), name='create_news'),
    path('news/<slug:news>/', news_detail, name='news_detail_page'),
    path('news/<slug>/edit', UpdateNewsView.as_view(), name='edit_news'),
    path('news/<slug>/delete', DeleteNewsView.as_view(), name='delete_news'),
    path('contact-us/', ContactPageView.as_view(), name='contact_page'),
    path('local/', LocalNewsView.as_view(), name='local_news_page'),
    path('foreign/', ForeignNewsView.as_view(), name='foreign_news_page'),
    path('techno/', TechnoNewsView.as_view(), name='techno_news_page'),
    path('sport/', SportNewsView.as_view(), name='sport_news_page'),
    path('admin-page/', admin_page_view, name='admin_page'),
    path('search-results/', SearchResaltView.as_view(), name='search_results')
]