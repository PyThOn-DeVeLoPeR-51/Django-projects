from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, CreateView, DeleteView
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin

from news_project.custom_permissions import OnlyLoggedSuperUser
from .models import News, Category
from .forms import ContactForm, CommentForm
from .admin import NewsAdmin


class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'


# class NewsDetailView(DetailView):
#     model = News
#     template_name = 'news/news_detail.html'


def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {}
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    comments = news.comments.filter(active=True)
    comment_count = comments.count()
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    context = {
        'news': news,
        'comments': comments,
        'comment_count': comment_count,
        'comment_form': comment_form,
        'new_comment': new_comment,
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
        news = self.model.published.all().filter(category__name='mahalliy')[:10]

        return news


class ForeignNewsView(ListView):
    model = News
    template_name = 'news/foreign_news.html'
    context_object_name = 'foreign_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='xorijiy')[:10]
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


class UpdateNewsView(OnlyLoggedSuperUser, UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'category', 'status')
    template_name = 'crud/update_news.html'


class DeleteNewsView(OnlyLoggedSuperUser, DeleteView):
    model = News
    template_name = 'crud/delete_news.html'
    success_url = reverse_lazy('home_page')


class CreateNewsView(OnlyLoggedSuperUser, CreateView):
    model = News
    fields = ('title', 'slug', 'body', 'image', 'category', 'status')
    template_name = 'crud/create_news.html'
    # slug_url_kwarg = NewsAdmin.prepopulated_fields


@login_required
@user_passes_test(lambda u:u.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)
    context = {
        'admin_users': admin_users
    }
    return render(request, 'pages/admin_page.html', context=context)


class SearchResaltView(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'all_news'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )





