from .models import Post, Category, SubscribeCategory, Author
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.core.paginator import Paginator


# Представление списка публикаций
class PostsList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 5


# Представление одиночной публикации
class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    # Добавляем в контекст инфу - состоит ли пользователь в группе authors
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_subscribe'] = self.request.user.groups.filter(name='authors').exists()
        return context


# Представление списка публикаций по выбранной категории
def posts_by_category(request, category_id):
    category = Category.objects.get(id=category_id)
    posts = Post.objects.filter(category=category)
    if request.user.is_authenticated:
        subscribed_categories = SubscribeCategory.objects.filter(user=request.user, category=category)
    else:
        subscribed_categories = None
    paginator = Paginator(posts, 5)  # не работает: на странице все равно более 5 постов выводится
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'posts_by_category.html',
              {'category': category,
               'posts': posts,
               'subscribed_categories': subscribed_categories,
               'page_obj': page_obj}
              )

# Представление подписок пользователя
def subscriptions(request):
    subscribe_categories = SubscribeCategory.objects.filter(user=request.user)
    return render(request, 'subscriptions.html', {'subscribe_categories': subscribe_categories})


# Представление поиска публикаций
class Search(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    ordering = ['-date']
    paginate_by = 5
    success_url = reverse_lazy('posts_list')

    # накладываем фильтр на данные запрашиваемые из базы
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
class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('main.add_post', )
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    # добавление в post запрос наименование категории, в зависимости от того, с какого url его отправляли - news
    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_category = 'Новость'
        post.author = Author.objects.get(user=self.request.user)
        return super().form_valid(form)


# Представление для создания статьи
class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('main.add_post', )
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'

    # добавление в post запрос наименование категории, в зависимости от того, с какого url его отправляли - article
    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_category = 'Статья'
        post.author = Author.objects.get(user=self.request.user)
        return super().form_valid(form)


# Представление для изменения поста
class PostsEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('main.change_post', )
    form_class = PostForm
    model = Post
    template_name = 'posts_edit.html'


# Представление для удаления поста.
class PostsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('main.delete_post', )
    model = Post
    template_name = 'posts_delete.html'
    success_url = reverse_lazy('posts')


# Представление для оформления подписки
@login_required
def subscribe_category(request, category_id):
    user = request.user
    category = Category.objects.get(id=category_id)
    subscribe_categories = SubscribeCategory.objects.filter(user=user, category=category).first()
    if not subscribe_categories:
        SubscribeCategory.objects.create(user=user, category=category)
    return redirect('posts_by_category', category_id=category_id)


# Представление для отмены подписки
@login_required
def unsubscribe_category(request, category_id):
    user = request.user
    category = Category.objects.get(id=category_id)
    SubscribeCategory.objects.filter(user=user, category=category).delete()
    return redirect('subscriptions')
