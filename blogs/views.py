from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from .utils import get_topics, check_topic_owner

# Create your views here.

def index(request):
    return render(request, 'blogs/index.html')

def get_recent_entries(request):
    topics = get_topics(request.user)
    flat_entries = []

    for entries in map(get_entries_for_topic, topics):
        for entry in entries:
            flat_entries.append(entry)

    sorted_entries = sorted(flat_entries, key=lambda entry: entry.date_added, reverse=True)
    return sorted_entries

def get_entries_for_topic(topic):
    return topic.entry_set.all()

def base_context(request):
    return {'recent_entries': get_recent_entries(request)}

@login_required()
def topics(request):
    topics = get_topics(request.user)
    context = {'topics': topics}
    context.update(base_context(request))
    return render(request, 'blogs/topics.html', context)

@login_required()
def topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    check_topic_owner(request, topic)

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    context.update(base_context(request))
    return render(request, 'blogs/topic.html', context)

@login_required()
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('blogs:topics'))

    context = {'form': form}
    context.update(base_context(request))
    return render(request, 'blogs/new_topic.html', context)

@login_required()
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        check_topic_owner(request, topic)
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('blogs:topic', args=[topic_id]))

    context = {'topic': topic, 'form': form}
    context.update(base_context(request))
    return render(request, 'blogs/new_entry.html', context)

@login_required()
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(request, topic)

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blogs:topic', args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    context.update(base_context(request))
    return render(request, 'blogs/edit_entry.html', context)

@login_required()
def delete_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(request, topic)

    if request.method == 'GET':
        entry.delete()
    return HttpResponseRedirect(reverse('blogs:topic', args=[topic.id]))


