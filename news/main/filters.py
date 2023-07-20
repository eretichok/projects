from django_filters import FilterSet, DateFilter, CharFilter, ModelChoiceFilter
from .models import Post, Category
from django.forms.widgets import DateInput


# поисковый фильтр
class PostFilter(FilterSet):
    headline = CharFilter(
        field_name='headline',
        label='Поиск по заголовку',
        lookup_expr='icontains',
    )

    category = ModelChoiceFilter(
        field_name='category',
        queryset=Category.objects.all(),
        label='Выбор категории',
        lookup_expr='exact',
    )

    # !!не получается настроить ModelChoiceFilter для post_category!!
    # post_category = ModelChoiceFilter(
    #     field_name='post_category',
    #     queryset=????????,
    #     label='Выбор раздела',
    #     lookup_expr='exact',
    # )

    date = DateFilter(
        field_name='date',
        label='Дата публикации начиная с',
        lookup_expr='gte',
        widget=DateInput(attrs={'type': 'date',}),
    )

    class Meta:
        model = Post
        fields = {'headline', 'category', 'post_category', 'date'}
