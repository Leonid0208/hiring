from django import forms
from django.forms import ModelForm
from .models import Message, Candidate


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        labels = {'message': ""}


class CreateResumeForm(ModelForm):
    class Meta:
        model = Candidate
        fields = ('title', 'location', 'salary', 'year_experience', 'description', 'addition', 'file')

