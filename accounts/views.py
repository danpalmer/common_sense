from django.http import HttpResponseRedirect
from django.views import generic as views
from django.contrib import messages
from django.core.urlresolvers import reverse

from .forms import ProfileEditForm
from .models import UserTopic


class ProfileEditView(views.FormView):
    form_class = ProfileEditForm
    template_name = 'accounts/profile_edit.html'

    def get_initial(self):
        return {
            'topics': UserTopic.objects.values_list('topic', flat=True),
        }

    def form_valid(self, form):
        form.save(self.request.user)
        messages.success(self.request, "Updated topics")
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('consultations:home')
