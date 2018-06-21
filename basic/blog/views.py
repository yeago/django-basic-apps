import re

from django.views.generic.dates import ArchiveIndexView
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.conf import settings

from basic.blog.models import Post, Category
from basic.tools.constants import STOP_WORDS_RE


class PostListCategory(ArchiveIndexView):
    paginate_by = 20
    date_field = 'publish'
    template_object_name = 'object_list'
    allow_future = False
    model = Post
    def get_queryset(self):
        queryset = super(PostListCategory, self).get_queryset()
        self.object = get_object_or_404(Category, slug=self.kwargs.get("slug"), site=settings.SITE_ID)
        return queryset.filter(categories=self.object).order_by('-publish')

    def get_context_data(self, **kwargs):
        context = super(PostListCategory, self).get_context_data(**kwargs)
        context['category'] = self.object
        return context


def search(request, template_name='blog/post_search.html'):
    """
    Search for blog posts.

    This template will allow you to setup a simple search form that will try to return results based on
    given search strings. The queries will be put through a stop words filter to remove words like
    'the', 'a', or 'have' to help imporve the result set.

    Template: ``blog/post_search.html``
    Context:
        object_list
            List of blog posts that match given search term(s).
        search_term
            Given search term.
    """
    context = {}
    if request.GET:
        stop_word_list = re.compile(STOP_WORDS_RE, re.IGNORECASE)
        search_term = '%s' % request.GET['q']
        cleaned_search_term = stop_word_list.sub('', search_term)
        cleaned_search_term = cleaned_search_term.strip()
        if len(cleaned_search_term) != 0:
            post_list = Post.objects.published().filter(Q(title__icontains=cleaned_search_term) | Q(body__icontains=cleaned_search_term) | Q(tags__icontains=cleaned_search_term) | Q(categories__title__icontains=cleaned_search_term))
            context = {'object_list': post_list, 'search_term':search_term}
        else:
            message = 'Search term was too vague. Please try again.'
            context = {'message':message}
    return render(request, template_name, context)
