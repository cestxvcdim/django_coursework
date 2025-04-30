from datetime import datetime, timedelta

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.cache import cache
from django.core.mail import send_mail

from config import settings
from mailing.models import Client, Mailing, MailingAttempt, Message


frequency_time = {
    'daily': timedelta(days=1),
    'weekly': timedelta(days=7),
    'monthly': timedelta(days=30),
}


def get_cached_client_info(client_id: int):
    if settings.CACHE_ENABLED:
        key = f'client_info_{client_id}'
        client_info = cache.get(key)
        if client_info is None:
            client = Client.objects.get(pk=client_id)
            email = client.email
            full_name = client.full_name
            client_info = {
                'email': email,
                'full_name': full_name,
            }
            cache.set(key, client_info)
    else:
        client = Client.objects.get(pk=client_id)
        email = client.email
        full_name = client.full_name
        client_info = {
            'email': email,
            'full_name': full_name,
        }

    return client_info


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, 'interval', seconds=10)
    scheduler.start()


def job():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    mailings = Mailing.objects.all()
    for mailing in mailings:
        update_status(mailing, current_datetime)


def update_status(mailing, current_datetime):
    if current_datetime < mailing.start_sending:
        mailing.status = 'created'
    elif mailing.start_sending <= current_datetime <= mailing.end_sending:
        mailing.status = 'started'
        attempt = MailingAttempt.objects.filter(mailing=mailing).order_by('-last_attempt').first()
        if attempt is None or attempt.last_attempt + frequency_time[mailing.frequency] <= current_datetime:
            send(mailing, current_datetime)
    else:
        mailing.status = 'finished'
    mailing.save()


def send(mailing, current_datetime):
    try:
        msg = Message.objects.get(mailing=mailing)
        send_mail(
            subject=msg.topic,
            message=msg.body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[client.email for client in mailing.clients.all()]
        )
        response = f"Рассылка была успешна проведена"
        status = True
    except Exception as e:
        response = f"Error {e}"
        status = False
    MailingAttempt.objects.create(
        last_attempt=current_datetime,
        is_sent=status,
        server_response=response,
        mailing=mailing
    )
