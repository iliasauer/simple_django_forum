# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models


class Forum(models.Model):
    class Meta:
        db_table = "forum"
    forum_title = models.CharField(max_length=100)
    forum_description = models.TextField(default='No description provided.')
    forum_creator = models.ForeignKey(User, blank=True, null=True)
    forum_created = models.DateTimeField(auto_now=True)
    forum_updated = models.DateTimeField(auto_now=True)

    def num_articles(self):
        return sum([topic.num_articles() for topic in self.topic_set.all()])

    def last_article(self):
        if self.topic_set.count():
            last_article = None
            for topic in self.topic_set.all():
                article = topic.last_article()
                if article:
                    if not last_article:
                        last_article = article
                    elif article.created > last_article.created:
                        last_article = article
            return last_article


class Topic(models.Model):
    class Meta:
        db_table = "topic"
    topic_title = models.CharField(max_length=100)
    topic_description = models.TextField(default='No description provided.')
    topic_forum = models.ForeignKey(Forum)
    topic_creator = models.ForeignKey(User, blank=True, null=True)
    topic_created = models.DateTimeField(auto_now=True)
    topic_updated = models.DateTimeField(auto_now=True)
    closed = models.BooleanField(default=False)

    def num_articles(self):
        return self.article_set.count()

    def num_replies(self):
        return max(0, self.article_set.count() - 1)

    def last_article(self):
        if self.article_set.count():
            return self.article_set.order_by("article_created")[0]


class Article(models.Model):
    class Meta:
        db_table = "article"
    article_title = models.CharField(max_length=200)
    article_text = models.TextField()
    article_creator = models.ForeignKey(User, blank=True, null=True)
    article_created = models.DateTimeField(auto_now_add=True)
    article_updated = models.DateTimeField(auto_now=True)
    article_topic = models.ForeignKey(Topic)
    article_user_ip = models.GenericIPAddressField(blank=True, null=True)

    def short(self):
        return u"%s - %s\n%s" % \
               (self.article_creator, self.article_title, self.article_created.strftime("%b %d, %I:%M %p"))

    short.allow_tags = True
