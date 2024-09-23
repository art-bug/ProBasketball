from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView

from .models import News
from .forms import ArticleForm


class NewsList(ListView):
    model = News
    template_name = 'news/news_list.html'
    ordering = '-published'
    paginate_by = 5
    context_object_name = 'news'


class ArticleFormView(FormView):
    form_class = ArticleForm
    template_name = 'news/article_creation.html'
    success_url = reverse_lazy('news-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {**context, 'title': 'Создать новость'}

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        form.errors = 'Неверная форма'
        return super().form_invalid(form)


class ArticleDetails(DetailView):
    model = News
    template_name = 'news/article_details.html'
    context_object_name = 'article'
    slug_url_kwarg = 'slug'
