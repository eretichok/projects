from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


# Модель авторов публикаций с привязкой к user
class Author(models.Model):
    rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    # метод перерасчета рейтинга автора
    def update_rating(self):
        rating = 0
        # достаем сумму рейтингов всех публикаций автора
        post_rat = self.post_set.aggregate(post_rating=Sum('rating'))
        rating += post_rat.get('post_rating') * 3
        # достаем сумму рейтингов всех комментариев автора
        com_rat = self.user.comment_set.aggregate(com_rating=Sum('rating'))
        rating += com_rat.get('com_rating')
        # достаем сумму рейтингов всех комментариев к публикациям автора
        com_auth_rat = Comment.objects.filter(post__author=self).aggregate(com_auth_rating=Sum('rating'))
        if com_auth_rat:
            rating += com_auth_rat.get('com_auth_rating')

        self.rating = rating
        self.save()

    # def r_self(self):
    #     print(self, '---', self.user)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


# Модель категорий для публикаций
class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category_name

ARTICLE = 'AR'
NEWS = 'NW'
POST_CATEGORY_CHOICES = [
    (ARTICLE, 'Статья'),
    (NEWS, 'Новость'),
]

# Модель публикаций
class Post(models.Model):

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_category = models.CharField(max_length=7, choices=POST_CATEGORY_CHOICES)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    headline = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    # метод для поднятия рейтинга публикации(like)
    def like(self):
        self.rating += 1
        self.save()

    # метод для понижения рейтинга публикации(dislike)
    def dislike(self):
        self.rating -= 1
        self.save()

    # метод возврата превью публикации
    def preview(self):
        return f'{self.text[:124]}...'

    # метод возврата адреса только что созданной публикации
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.headline}: {self.text[:20]}' + '...'


# Модель связки публикация с категориями (many_to_many)
class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


# Модель комментариев к публикациям
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    # метод для поднятия рейтинга публикации(like)
    def like(self):
        self.rating += 1
        self.save()

    # метод для понижения рейтинга публикации(dislike)
    def dislike(self):
        self.rating -= 1
        self.save()


