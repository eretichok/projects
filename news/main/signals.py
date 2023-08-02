from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Post, SubscribeCategory
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.conf import settings


# рассылка подписчикам: новая публикация в категории, на которую пользователи подписаны
@receiver(m2m_changed, sender=Post.category.through)
def notify_subscribers(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        post_categories = instance.category.filter(pk__in=pk_set).distinct()
        email_list = SubscribeCategory.objects.filter(category__in=post_categories).values_list('user__email',
                                                                                                flat=True).distinct()
        post_categories_name = ', '.join(instance.category.values_list('category_name', flat=True))
        if email_list:
            for email in email_list:
                subject = f"Вышла новая публикация в категории {post_categories_name}."
                message = render_to_string('post_created.html', {'post': instance})
                send_mail(
                                subject=subject,
                                message=message,
                                from_email=settings.DEFAULT_FROM_EMAIL,
                                recipient_list=[email]
                            )


# сигнал, отправляющий письмо новому зарегистрированному пользователю
@receiver(post_save, sender=User)
def notify_new_user(sender, instance, created, **kwargs):
    if created:
        message = render_to_string('new_user_mail.html', {'user': instance})
        subject = f'Добро пожаловать, {instance.first_name} {instance.last_name}!'
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email]
            )