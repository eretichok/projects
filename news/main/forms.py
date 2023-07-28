from django import forms
from .models import Post, Author
from django.core.exceptions import ValidationError


# форма создания публикации
class PostForm(forms.ModelForm):
    # простые проверки до обращения к базе без переопределения метода clean()
    headline = forms.CharField(min_length=3)
    text = forms.CharField(min_length=3)

    class Meta:
        model = Post
        fields = ['headline', 'text', 'author', 'category']
        labels = {
            'headline': 'Заголовок',
            'text': 'Поиск в тексте публикации',
            'author': 'Автор',
            'category': 'Категория',
        }

    # переопределения метода clean с целью проверки входящих данных до обращения к базе
    def clean(self):
        cleaned_data = super().clean()
        headline = cleaned_data.get("headline")
        text = cleaned_data.get("text")
        if headline == text:
            raise ValidationError({
                "text": "Заголовок не может быть содержанием."
            })

        return cleaned_data

