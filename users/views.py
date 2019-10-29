from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm
from .models import CustomUser

# Create your views here.
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class PassRequestToFormViewMixin:
    def get_form_kwargs(self):
        kwargs = super(PassRequestToFormViewMixin, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class UserDetailView(PassRequestToFormViewMixin, TemplateView):
    template_name = 'user_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user'] = self.request.user
        return context

class UpdateUserView(LoginRequiredMixin, UpdateView):
    template_name = 'user_edit.html'
    model = CustomUser
    fields = ('first_name', 'last_name', 'username', 'email')
    success_url = reverse_lazy('profile')
    login_url = 'login'
    
    