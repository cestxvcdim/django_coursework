from django.db import models

NULLABLE = {'blank': True, 'null': True}

FREQUENCY_CHOICES = [
    ('daily', 'ежедневно'),
    ('weekly', 'еженедельно'),
    ('monthly', 'ежемесячно'),
]

STATUS_CHOICES = [
    ('created', 'создана'),
    ('started', 'запущена'),
    ('finished', 'закончена'),
]


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='почта')
    full_name = models.CharField(max_length=150, verbose_name='ФИО')
    commentary = models.TextField(**NULLABLE, verbose_name='комментарий')

    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, **NULLABLE, verbose_name='пользователь')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Message(models.Model):
    topic = models.CharField(max_length=50, verbose_name='тема письма')
    body = models.TextField(verbose_name='содержание письма')

    author = models.ForeignKey('users.User', on_delete=models.SET_NULL, **NULLABLE, verbose_name='автор письма')

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = 'письмо'
        verbose_name_plural = 'письма'


class Mailing(models.Model):
    start_sending = models.DateTimeField(verbose_name='дата начала рассылки')
    end_sending = models.DateTimeField(verbose_name='дата окончания рассылки')
    frequency = models.CharField(choices=FREQUENCY_CHOICES, verbose_name='частота отправки')
    status = models.CharField(choices=STATUS_CHOICES, verbose_name='статус')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='письмо')
    clients = models.ManyToManyField(Client, verbose_name='клиенты')

    creator = models.ForeignKey('users.User', on_delete=models.SET_NULL, **NULLABLE, verbose_name='создатель рассылки')

    def __str__(self):
        return f'start: {self.start_sending}, end: {self.end_sending}, msg: {self.message}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class MailingAttempt(models.Model):
    last_attempt_time = models.DateTimeField(auto_now_add=True, verbose_name='время последней попытки')
    is_sent = models.BooleanField(default=False, verbose_name='отправлено?')
    server_response = models.CharField(max_length=100, verbose_name='ответ сервера')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка')

    def __str__(self):
        return f'last attempt: {self.last_attempt_time}, mailing: ({self.mailing}), server response: {self.server_response}'

    class Meta:
        verbose_name = 'попытка рассылки'
        verbose_name_plural = 'попытки рассылок'
