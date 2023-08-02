from django.urls import path
# from django.contrib.auth.views import LoginView, LogoutView
from .views import ProfileView, ProfileEditView, upgrade_me

urlpatterns = [
    # path('login/', LoginView.as_view(template_name='login.html'), name='login'), # реализовано через OAuth
    # path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'), # реализовано через OAuth
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:id>/', ProfileEditView.as_view(), name='profile_edit'),
    # path('signup/', LogoutView.as_view(template_name='signup.html'), name='signup'), # реализовано через OAuth
    path('upgrade/', upgrade_me, name='upgrade')
]