# from django.contrib.auth.models import User
# from .forms import BaseRegisterForm
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

# представление профиля
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
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
    return redirect('/')
