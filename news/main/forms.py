from django import forms
from .models import Post, Category
from django.core.exceptions import ValidationError


# форма создания публикации
class PostForm(forms.ModelForm):
    # простые проверки до обращения к базе без переопределения метода clean()
    headline = forms.CharField(min_length=3, label='Заголовок')
    text = forms.CharField(min_length=10, label='Текст публикации')
    category = forms.ModelMultipleChoiceField(
        label='Категория',
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Post
        fields = ['headline', 'text', 'category']

    # переопределения метода clean с целью проверки входящих данных до обращения к базе
    def clean(self):
        cleaned_data = super().clean()
        headline = cleaned_data.get("headline")
        text = cleaned_data.get("text")
        if headline == text:
            raise ValidationError({"text": "Заголовок не может быть содержанием."})
        return cleaned_data
