from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_managers
from .models import Post
from django.core.mail import send_mail


@receiver(post_save, sender=Post)
def notify_new_post(sender, instance, created, **kwargs):
    if created:
        subject = f'Создана публикация в разделе {instance.post_category}.Тема {instance.headline}'
    else:
        subject = f'Публикация {instance.headline} изменена.'

    send_mail(
        subject=subject,
        message=instance.text,
        from_email='eretichok@yandex.ru',
        recipient_list=['7100355@gmail.com']
        )
