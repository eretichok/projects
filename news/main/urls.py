from django.urls import path
from .views import PostsList, PostDetail, Search
from .views import NewsCreate, ArticleCreate, PostsEdit, PostsDelete
from .views import subscriptions, subscribe_category, unsubscribe_category, posts_by_category

urlpatterns = [
    # для любых пользователей
    path('', PostsList.as_view(), name='posts'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('search/', Search.as_view(), name='search'),
    path('category/', PostsList.as_view(), name='category'),
    path('category/<int:category_id>/', posts_by_category, name='posts_by_category'),
    # для зарегистрированных пользователей
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('category/<int:category_id>/subscribe/', subscribe_category, name='subscribe_category'),
    path('category/<int:category_id>/unsubscribe/', unsubscribe_category, name='unsubscribe_category'),
    # для пользователей из группы author
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('article/create/', ArticleCreate.as_view(), name='article_create'),
    path('<int:pk>/edit/', PostsEdit.as_view(), name='posts_edit'),
    path('<int:pk>/delete/', PostsDelete.as_view(), name='posts_delete'),
]
