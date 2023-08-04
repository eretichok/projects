from celery import shared_task
from django.template.loader import render_to_string
from datetime import datetime, timedelta
from main.models import SubscribeCategory, Category, Post
from django.core.mail import send_mail
from django.conf import settings


# задача: еженедельная рассылка новых постов подписчикам на категории
@shared_task
def weekly_send_mail():
    today = datetime.today()  # сегодня
    week_ago = today - timedelta(days=7)  # дата неделю назад
    # находим почту всех пользователей имеющих подписки
    email_list = SubscribeCategory.objects.values_list('user__email', flat=True).distinct()
    for email in email_list:
        # находим для все категории на которые подписан данный user
        user_subscribed_categories = SubscribeCategory.objects.filter(user__email=email).values_list('category',
                                                                                                     flat=True)
        posts_list = Post.objects.filter(category__in=user_subscribed_categories, date__gte=week_ago)
        categories_names = Category.objects.filter(id__in=user_subscribed_categories).values_list('category_name',
                                                                                                  flat=True)
        if posts_list:
            subject = f'Еженедельная подборка новых публикаций.'
            message = render_to_string(
                'weekly_newsletter.html', {'posts': posts_list,
                                           'categories_names': categories_names}
            )
            send_mail(subject, message, 'eretichok@yandex.ru', [email], fail_silently=False)


# задача: рассылка подписчикам на категорию нового поста (проверка раз в 1 минуту)
@shared_task
def new_post_mail(post):
    post_categories = post.category.all()
    email_list = SubscribeCategory.objects.filter(category__in=post_categories).values_list('user__email',
                                                                                            flat=True).distinct()
    post_categories_name = ', '.join(post_categories.values_list('category_name', flat=True))
    if email_list:
        for email in email_list:
            subject = f"Вышла новая публикация в категории {post_categories_name}."
            message = render_to_string('post_created.html', {'post': post})
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email]
            )
