# from .forms import BaseRegisterForm
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from main.models import Author
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy


# представление профиля
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context['groups'] = self.request.user.groups.all()
        return context


# представление формы регистрации. Заменена на OAuth.
# class BaseRegisterView(CreateView):
#     model = User
#     form_class = BaseRegisterForm
#     success_url = '/'


# функция "Хочу стать автором!"
@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    Author.objects.create(name=request.user.username, user=request.user)
    return redirect('/profile/')


# Представление для изменения профиля
class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'profile_edit.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('profile')