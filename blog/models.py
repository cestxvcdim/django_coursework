from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='заголовок')
    body = models.TextField(verbose_name='содержимое')
    image = models.ImageField(upload_to='posts/', **NULLABLE, verbose_name='изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    is_published = models.BooleanField(default=True, verbose_name='опубликовано?')
    views_count = models.IntegerField(default=0, verbose_name='счетчик просмотров')

    author = models.ForeignKey('users.User', on_delete=models.SET_NULL, **NULLABLE, verbose_name='автор')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
