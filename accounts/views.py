from django.views import generic as views

from .forms import TopicEditForm


class TopicEditView(views.FormView):
    form_class = TopicEditForm
    template_name = 'accounts/topics.html'
