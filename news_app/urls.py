from django.urls import path
from .views import NewsListView, news_detail, HomePageView, ContactPageView, LocalNewsView, \
    ForeignNewsView, TechnoNewsView, SportNewsView

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('all-news/', NewsListView.as_view(), name='news_list'),
    path('news/<slug:news>/', news_detail, name='news_detail_page'),
    path('contact-us/', ContactPageView.as_view(), name='contact_page'),
    path('local/', LocalNewsView.as_view(), name='local_news_page'),
    path('foreign/', ForeignNewsView.as_view(), name='foreign_news_page'),
    path('techno/', TechnoNewsView.as_view(), name='techno_news_page'),
    path('sport/', SportNewsView.as_view(), name='sport_news_page'),
]