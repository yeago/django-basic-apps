from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.contrib.auth.models import User

from basic.blog.managers import PublicManager

import datetime
from tagging.fields import TagField
from django.contrib.sites.models import Site


class Category(models.Model):
    """Category model."""
    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    site = models.ForeignKey('sites.Site')

    def save(self, *args, **kwargs):
        self.site = Site.objects.get_current()
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        db_table = 'blog_categories'
        ordering = ('title',)

    def __unicode__(self):
        return u'%s' % self.title

    def __str__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return ('blog_category_detail', None, {'slug': self.slug})


class Post(models.Model):
    """Post model."""
    STATUS_CHOICES = (
        (1, _('Draft')),
        (2, _('Public')),
    )
    site = models.ForeignKey('sites.Site')
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), unique_for_date='publish')
    author = models.ForeignKey(User, blank=True, null=True)
    body = models.TextField(_('body'), )
    tease = models.TextField(_('tease'), blank=True, help_text=_('Concise text suggested. Does not appear in RSS feed.'))
    status = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=2)
    allow_comments = models.BooleanField(_('allow comments'), default=True)
    publish = models.DateTimeField(_('publish'), default=datetime.datetime.now)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    categories = models.ManyToManyField(Category, blank=True)
    tags = TagField()
    objects = PublicManager()
    followup_to = models.ForeignKey('Post', null=True, blank=True, related_name="followup_set",
                                    help_text="Links to the previous post in a series")

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        db_table = 'blog_posts'
        ordering = ('-publish',)
        get_latest_by = 'publish'
        permissions = [
            ('post_editor', 'Post Editor'),
        ]

    def __unicode__(self):
        return u'%s' % self.title

    def __str__(self):
        return self.title

    def get_deferred_fields(self):
        # Make tags not deferred
        deferred_set = super(Post, self).get_deferred_fields()
        return {f for f in deferred_set if f != 'tags'}

    def save(self, *args, **kwargs):
        self.site = Site.objects.get_current()
        super(Post, self).save(*args, **kwargs)

    @permalink
    def get_absolute_url(self):
        return ('blog_detail', None, {
            'year': self.publish.year,
            'month': self.publish.strftime('%b').lower(),
            'day': self.publish.day,
            'slug': self.slug
        })

    def get_previous_post(self):
        return self.get_previous_by_publish(status__gte=2)

    def get_next_post(self):
        return self.get_next_by_publish(status__gte=2)


class BlogRoll(models.Model):
    """Other blogs you follow."""
    name = models.CharField(max_length=100)
    url = models.URLField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('sort_order', 'name',)
        verbose_name = _('blog roll')
        verbose_name_plural = _('blog roll')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.url
