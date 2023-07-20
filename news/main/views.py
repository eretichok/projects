from .models import Post, Author
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy


# Представление списка публикаций
class PostsList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 3


# Представление одиночной публикации
class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


# Представление поиска публикаций
class Search(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    ordering = ['-date']
    paginate_by = 5
    success_url = reverse_lazy('posts_list')

    # накладываем фильтр данные запрашиваемые из базы
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

    # функция возврата списка товаров по заданным критериям
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs


# Представление для создания новости
class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    # добавление в post запрос наименование категории, в зависимости от того, с какого url его отправляли - news
    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_category = 'Новость'
        # post.author = self.request.author
        return super().form_valid(form)

# Представление для создания статьи
class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'

    # добавление в post запрос наименование категории, в зависимости от того, с какого url его отправляли - article
    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_category = 'Статья'
        # post.author = self.request.author
        return super().form_valid(form)


# Представление для изменения поста
class PostsEdit(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'posts_edit.html'


# Представление для удаления поста.
class PostsDelete(DeleteView):
    model = Post
    template_name = 'posts_delete.html'
    success_url = reverse_lazy('posts')
