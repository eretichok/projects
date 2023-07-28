from django_filters import FilterSet, DateFilter, CharFilter, ModelChoiceFilter, ChoiceFilter
from .models import Post, Category, POST_CATEGORY_CHOICES
from django.forms.widgets import DateInput
from django import forms


# поисковый фильтр
class PostFilter(FilterSet):
    headline = CharFilter(
        field_name='headline',
        label='Поиск по заголовку',
        lookup_expr='icontains',
    )

    category = ModelChoiceFilter(
        empty_label='все категории',
        field_name='category',
        queryset=Category.objects.all(),
        label='Выбор категории',
        lookup_expr='exact',
    )

    post_category = ChoiceFilter(
        empty_label='все разделы',
        choices=POST_CATEGORY_CHOICES,
        field_name='post_category',
        label='Выбор раздела',
        lookup_expr='exact',
    )

    date = DateFilter(
        field_name='date',
        label='Дата публикации начиная с',
        lookup_expr='gte',
        widget=DateInput(attrs={'type': 'date',}),
    )

    class Meta:
        model = Post
        fields = {'headline', 'category', 'post_category', 'date'}
