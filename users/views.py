from django.contrib.auth.views import LoginView
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, CreateView

from users.forms import UserLoginForm


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        redirect_page = self.request.GET.get('next')
        if redirect_page and redirect_page != reverse('users:logout'):
            return redirect_page
        return reverse_lazy('main:index')


class UserRegistrationView(CreateView):
    pass


class UserProfileView(UpdateView):
    pass
