from django import forms

from consultations.models import Topic


class ProfileEditForm(forms.Form):
    topics = forms.ModelMultipleChoiceField(
        queryset=Topic.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    def save(self, user):
        user.topics.all().delete()

        for topic in self.cleaned_data['topics']:
            user.topics.create(
                topic=topic,
            )
