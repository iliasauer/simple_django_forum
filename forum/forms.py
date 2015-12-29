from django.forms import ModelForm

from forum.models import Article, Topic


class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['topic_title', 'topic_description']


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['article_title', 'article_text']
