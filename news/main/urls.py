from django.urls import path
from .views import PostsList, PostDetail, Search
from .views import NewsCreate, ArticleCreate, PostsEdit, PostsDelete


urlpatterns = [
    path('', PostsList.as_view(), name='posts'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('search/', Search.as_view(), name='search'),
    # path('profile/', PostsSearch.as_view(), name='profile'),

    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('article/create/', ArticleCreate.as_view(), name='article_create'),
    path('<int:pk>/edit/', PostsEdit.as_view(), name='posts_edit'),
    path('<int:pk>/delete/', PostsDelete.as_view(), name='posts_delete'),
]
