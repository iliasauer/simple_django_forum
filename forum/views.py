from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render_to_response, redirect
from django.template.context_processors import csrf

from forum.forms import ArticleForm, TopicForm
from forum.models import Forum, Topic, Article


def index(request):
    return redirect('/articles/all/')


def forums(request, page_number=1):
    all_forums = Forum.objects.all()
    current_page = Paginator(all_forums, 3)
    return render_to_response('list.html',
                              {'forums': current_page.page(page_number),
                               'username': auth.get_user(request).username})


def forum(request, forum_id=1, page_number=1):
    topic_form = TopicForm()
    args = {}
    args.update(csrf(request))
    topics = Topic.objects.filter(forum=forum_id).order_by("-topic_created")
    current_page = Paginator(topics, 3)
    args['topics'] = current_page.page(page_number)
    args['form'] = topic_form
    args['forum_id'] = forum_id
    return render_to_response('forum.html', args)


def topic(request, topic_id=1, page_number=1):
    article_form = ArticleForm()
    args = {}
    args.update(csrf(request))
    current_topic = Topic.objects.get(pk=topic_id)
    articles = Article.objects.filter(topic=topic_id).order_by("-article_created")
    current_page = Paginator(articles, 3)
    args['topic'] = current_topic
    args['form'] = article_form
    args['articles'] = current_page.page(page_number)
    return render_to_response('topic.html', args)


def reply(request, topic_id):
    current_topic = Topic.objects.get(pk=topic_id)
    if request.POST:
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.article_topic = current_topic
            article.creator = auth.get_user(request).username
            form.save()
    return redirect('/topic/get/%s/' % topic_id)


def addtopic(request, forum_id):
    current_forum = Forum.objects.get(pk=forum_id)
    if request.POST:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            # new_topic.topic_title = form.cleaned_data['topic_title']
            # new_topic.topic_description = form.cleaned_data['topic_description']
            new_topic.topic_forum = current_forum
            new_topic.topic_creator = auth.get_user(request).username
            new_topic.save()
    return redirect('/forum/get/%s/' % forum_id)

