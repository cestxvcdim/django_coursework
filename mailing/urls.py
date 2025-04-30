from django.urls import path
from django.views.decorators.cache import cache_page

from mailing import views
from mailing.apps import MailingConfig

app_name = MailingConfig.name

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('contacts/', cache_page(60)(views.contacts), name='contacts'),
    path('my_clients/', views.ClientListView.as_view(), name='client_list'),
    path('my_clients/<int:pk>/', views.ClientDetailView.as_view(), name='client_detail'),
    path('my_clients/create/', views.ClientCreateView.as_view(), name='client_create'),
    path('my_clients/<int:pk>/update/', views.ClientUpdateView.as_view(), name='client_update'),
    path('my_clients/<int:pk>/delete/', views.ClientDeleteView.as_view(), name='client_delete'),
    path('my_mailings/', views.MailingListView.as_view(), name='mailing_list'),
    path('my_mailings/<int:pk>/', views.MailingDetailView.as_view(), name='mailing_detail'),
    path('my_mailings/create/', views.MailingCreateView.as_view(), name='mailing_create'),
    path('my_mailings/<int:pk>/update/', views.MailingUpdateView.as_view(), name='mailing_update'),
    path('my_mailings/<int:pk>/delete/', views.MailingDeleteView.as_view(), name='mailing_delete'),
]
