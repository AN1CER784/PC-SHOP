
from django.urls import path
from users.views import UserProfileView, UserRegistrationView, UserLoginView
from django.contrib.auth.views import LogoutView
app_name = 'users'
urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout')

]

