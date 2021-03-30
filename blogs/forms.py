from django import forms
from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'text']
        labels = {'text': 'Text', 'title': 'Title'}
        widgets = {
            'title': forms.TextInput(attrs={'cols':20}),
            'text': forms.Textarea(attrs={'cols':80})
        }

