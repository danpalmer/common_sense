from django import forms

from .models import UserTopic


class TopicEditForm(forms.Form):
    topics = forms.ModelMultipleChoiceField(
        queryset=UserTopic.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
