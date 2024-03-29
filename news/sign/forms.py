# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

# простая форма регистрации by django. Заменена на OAuth
# class BaseRegisterForm(UserCreationForm):
#     email = forms.EmailField(label="Email")
#     first_name = forms.CharField(label="Имя")
#     last_name = forms.CharField(label="Фамилия")
#
#     class Meta:
#         model = User
#         fields = ("username",
#                   "first_name",
#                   "last_name",
#                   "email",
#                   "password1",
#                   "password2", )


# переопределение формы регистрации OAuth: новые пользователи автоматически попадают в группу common
class BasicSignupForm(SignupForm):
    email = forms.EmailField(label="Email", required=True)
    first_name = forms.CharField(max_length=30, label="Имя", required=True)
    last_name = forms.CharField(max_length=30, label="Фамилия")
    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",)

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
