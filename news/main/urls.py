from django.urls import path
from .views import PostsList, PostDetail, Search, CategorySubscribe
from .views import NewsCreate, ArticleCreate, PostsEdit, PostsDelete
from django.urls import include

urlpatterns = [
    # для любых пользователей
    path('', PostsList.as_view(), name='posts'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('search/', Search.as_view(), name='search'),
    # для пользователей из группы author
    path('category_subscribe/', CategorySubscribe.as_view(), name='subscribe'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('article/create/', ArticleCreate.as_view(), name='article_create'),
    path('<int:pk>/edit/', PostsEdit.as_view(), name='posts_edit'),
    path('<int:pk>/delete/', PostsDelete.as_view(), name='posts_delete'),
]
