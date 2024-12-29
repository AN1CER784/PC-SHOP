from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import UpdateView, CreateView

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        redirect_page = self.request.GET.get('next')
        if redirect_page and redirect_page != reverse('users:logout'):
            return redirect_page
        return reverse('users:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Sign in'
        return context


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Sign up'
        return context

    def form_valid(self, form):
        user = form.save()
        auth.login(self.request, user)
        return redirect('users:profile')


class UserProfileView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Home - Profile'
        return context

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('users:profile')

    def form_valid(self, form):
        return super().form_valid(form)
