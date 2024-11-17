from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from .models import News, Category
from .forms import ContactForm


class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'


# class NewsDetailView(DetailView):
#     model = News
#     template_name = 'news/news_detail.html'


def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {
        'news': news
    }

    return render(request, 'news/news_detail.html', context=context)


class HomePageView(ListView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.all().order_by('-publish_time')[:5]
        context['local_news'] = News.published.all().filter(category__name='mahalliy').order_by('-publish_time')[:5]
        context['foreign_news'] = News.published.all().filter(category__name='xorijiy').order_by('-publish_time')[:5]
        context['techno_news'] = News.published.all().filter(category__name='texnologiya').order_by('-publish_time')[:5]
        context['sport_news'] = News.published.all().filter(category__name='sport').order_by('-publish_time')[:5]
        return context


class ContactPageView(TemplateView):
    template_name = 'news/contact.html'

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == "POST" and form.is_valid():
            form.save()
            return HttpResponse("Thank you for contact us!")
        context = {
            'form': form
        }

        return render(request, 'news/contact.html', context=context)

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            'form': form
        }

        return render(request, 'news/contact.html', context=context)


# def contactPageView(request):
#     form = ContactForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         form.save()
#         return HttpResponse("Thank you for contact us!")
#     context = {
#         'form': form
#     }
#
#     return render(request, 'news/contact.html', context=context)


class LocalNewsView(ListView):
    model = News
    template_name = 'news/local_news.html'
    context_object_name = 'local_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='mahalliy')[:5]

        return news


class ForeignNewsView(ListView):
    model = News
    template_name = 'news/foreign_news.html'
    context_object_name = 'foreign_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='xorijiy')
        return news
    
    
class TechnoNewsView(ListView):
    model = News
    template_name = 'news/techno_news.html'
    context_object_name = 'techno_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='texnologiya')
        return news
    
    
class SportNewsView(ListView):
    model = News
    template_name = 'news/sport_news.html'
    context_object_name = 'sport_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='sport')
        return news





