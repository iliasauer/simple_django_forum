from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'forum.views.index'),
    url(r'^forum/all/$', 'forum.views.forums'),
    url(r'^forum/get/(?P<forum_id>[0-9]+)/$', 'forum.views.forum'),
    url(r'^topic/get/(?P<topic_id>[0-9]+)/$', 'forum.views.topic'),
    url(r'^topic/get/(?P<topic_id>[0-9]+)/article/$', 'forum.views.reply'),
    url(r'^forum/get/(?P<forum_id>[0-9]+)/topic/$', 'forum.views.addtopic'),

]
