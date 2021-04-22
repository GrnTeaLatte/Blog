from .models import Topic
from django.http import Http404


def get_topics(user):
    topics = Topic.objects.filter(owner=user).order_by('date_added')
    return topics

def check_topic_owner(request, topic):
    if topic.owner != request.user:
        raise Http404
