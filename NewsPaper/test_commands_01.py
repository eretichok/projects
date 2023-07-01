from news.models import *

# Создать двух пользователей (с помощью метода User.objects.create_user('username')).
u1 = User.objects.create_user('Иван')
u2 = User.objects.create_user('Михаил')

# Создать два объекта модели Author, связанные с пользователями
auth1 = Author.objects.create(user=u1)
auth2 = Author.objects.create(user=u2)

# Добавить 4 категории в модель Category.
c1 = Category.objects.create(category_name='Мир')
c2 = Category.objects.create(category_name='Экономика')
c3 = Category.objects.create(category_name='Культура')
c4 = Category.objects.create(category_name='Наука')

# Добавить 2 статьи и 1 новость.
p1 = Post.objects.create(author=auth1, post_category='Статья', headline='Cтатья 1', text='Текст статьи 1')
p2 = Post.objects.create(author=auth2, post_category='Статья', headline='Cтатья 2', text='Текст статьи 2')
p3 = Post.objects.create(author=auth1, post_category='Новость', headline='Новость 1', text='Текст новости 1')

# Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
PostCategory.objects.create(post=p1, category=c2)
PostCategory.objects.create(post=p2, category=c1)
PostCategory.objects.create(post=p2, category=c3)
PostCategory.objects.create(post=p3, category=c4)

# Создать минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть минимум один комментарий).
com1 = Comment.objects.create(post=p1, user=u1, text='Хорошая статья')
com2 = Comment.objects.create(post=p2, user=u2, text='Отличная статья')
com3 = Comment.objects.create(post=p3, user=u1, text='Хорошая новость')
com4 = Comment.objects.create(post=p3, user=u2, text='Отличная новость')
com5 = Comment.objects.create(post=p2, user=u1, text='Великолепная статья')

# Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
p1.like()
p1.like()
p1.dislike()
p2.like()
p2.like()
p3.like()
p3.like()
p3.like()
p3.like()
p3.dislike()

com1.like()
com1.like()
com1.dislike()
com2.like()
com2.like()
com3.like()
com3.like()
com3.like()
com3.like()
com3.dislike()
com4.like()
com4.like()
com4.like()
com4.like()
com4.like()
com4.dislike()
com5.like()
com5.like()
com5.like()
com5.like()
com5.like()

# Обновить рейтинги пользователей.
auth1.update_rating()
auth2.update_rating()

# Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
best_auth = Author.objects.order_by('-rating').values('user__username', 'rating').first()
print(f'Автор {best_auth["user__username"]} имеет наивысший рейтинг среди всех - {best_auth["rating"]}')

# Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи,
# основываясь на лайках/дислайках к этой статье.
best_article = Post.objects.filter(post_category='Статья').order_by('-rating').first()
print(f'Лучшая статья: {best_article.headline}. Ее рейтинг - {best_article.rating}\n'
      f'Ее написал {str(best_article.date).split()[0]} автор {best_article.author.user}\n'
      f'Предварительный просмотр статьи: {best_article.preview()}')

# Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
best_article_comments = Comment.objects.filter(post=best_article)
for i, comment in enumerate(best_article_comments):
    print(f'Комментарий №{i+1}: дата - {str(comment.date).split()[0]}, написал - {comment.user.username}, '
          f'рейтинг - {comment.rating}, текст - {comment.text}')