from django.urls import path
from django.views.decorators.cache import cache_page

from mailing import views
from mailing.apps import MailingConfig

app_name = MailingConfig.name

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('contacts/', cache_page(60)(views.contacts), name='contacts'),
]
