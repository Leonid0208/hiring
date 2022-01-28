from django.db import models
from app.models import CustomUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.shortcuts import reverse
from app.models import CustomUser
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError


class Chat(models.Model):
    DIALOG = 'D'
    CHAT = 'C'
    CHAT_TYPE_CHOICES = (
        (DIALOG, _('Dialog')),
        (CHAT, _('Chat'))
    )

    type = models.CharField(
        _('Тип'),
        max_length=1,
        choices=CHAT_TYPE_CHOICES,
        default=DIALOG
    )
    members = models.ManyToManyField(CustomUser, verbose_name=_("Участник"))

    def get_absolute_url(self):
        return reverse('messages', kwargs={'chat_id': self.pk})


class Message(models.Model):
    chat = models.ForeignKey(Chat, verbose_name=_("Чат"), on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, verbose_name=_("Пользователь"), on_delete=models.CASCADE)
    message = models.TextField(_("Сообщение"))
    pub_date = models.DateTimeField(_('Дата сообщения'), default=timezone.now)
    is_readed = models.BooleanField(_('Прочитано'), default=False)

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.message


def user_directory_path(instance, filename):
  
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.username, filename)


def file_size(value):
    limit = 1 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 1 MiB.')


class Candidate(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    location = models.CharField(max_length=150)
    salary = models.IntegerField()
    year_experience = models.IntegerField()
    description = RichTextField()
    addition = RichTextField()
    file = models.FileField(blank=True, null=True, default=None, upload_to=user_directory_path, validators=[file_size])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})
