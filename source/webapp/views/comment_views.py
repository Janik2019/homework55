from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView

from webapp.forms import CommentForm, ArticleCommentForm
from webapp.models import Comment, Article


class CommentListView(ListView):
    context_object_name = 'comments'
    model = Comment
    template_name = 'comment/list.html'
    ordering = ['-created_at']


class CommentForArticleCreateView(CreateView):
    template_name = 'comment/create.html'
    form_class = ArticleCommentForm

    def form_valid(self, form):
        article_pk = self.kwargs.get('pk')
        article = get_object_or_404(Article, pk=article_pk)
        article.comments.create(**form.cleaned_data)
        return redirect('article_view', pk=article_pk)


class CommentCreateView(CreateView):
    model = Comment
    template_name = 'comment/create.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('article_view', kwargs={'pk': self.object.article.pk})
