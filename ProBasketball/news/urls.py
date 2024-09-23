from django.urls import path

from .views import NewsList, ArticleFormView, ArticleDetails

urlpatterns = [
    path('', NewsList.as_view(), name='news-list'),
    path('create', ArticleFormView.as_view(), name='article-creation'),
    path('<str:slug>', ArticleDetails.as_view(), name='article-details')
]
