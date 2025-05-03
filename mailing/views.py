from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy, reverse

from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.services import get_random_posts
from mailing.forms import ClientForm, MailingForm, MessageForm
from mailing.models import Client, Mailing, Message
from mailing.services import get_cached_client_info


class HomeView(TemplateView):
    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['posts'] = get_random_posts()
        context_data['total_mailings'] = Mailing.objects.count()
        context_data['active_mailings'] = Mailing.objects.filter(status='started').count()
        context_data['unique_clients'] = Client.objects.count()
        return context_data


@login_required
def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'name: {name}\nphone: {phone}\nmessage: {message}')
    return render(request, 'mailing/contacts.html')


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        if user.groups.filter(name="Manager").exists() or user.is_superuser:
            context_data['object_list'] = Client.objects.all()
        else:
            context_data['object_list'] = Client.objects.filter(user=user)
        return context_data


class ClientDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Client

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        client_info = get_cached_client_info(kwargs['object'].pk)
        context_data['client_email'] = client_info['email']
        context_data['client_full_name'] = client_info['full_name']
        return context_data

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user == self.get_object().user or user.groups.filter(name="Manager").exists()


class ClientCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        if form.is_valid():
            client = form.save()
            user = self.request.user
            client.user = user
            client.save()

        return super().form_valid(form)

    def test_func(self):
        user = self.request.user
        return not user.groups.filter(name="Manager").exists()


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('mailing:client_detail', args=[self.kwargs['pk']])

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user == self.get_object().user


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user == self.get_object().user


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        if user.groups.filter(name="Manager").exists() or user.is_superuser:
            context_data['object_list'] = Mailing.objects.all()
        else:
            context_data['object_list'] = Mailing.objects.filter(creator=user)
        return context_data


class MailingDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Mailing

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user == self.get_object().creator or user.groups.filter(name="Manager").exists()


class MailingCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MessageFormset = inlineformset_factory(Mailing, Message, form=MessageForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = MessageFormset(self.request.POST)
        else:
            context_data['formset'] = MessageFormset()
        return context_data

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['clients'].queryset = Client.objects.filter(user=self.request.user)
        return form

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if form.is_valid():
            user = self.request.user
            self.object.creator = user
            self.object.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)

    def test_func(self):
        user = self.request.user
        return not user.groups.filter(name="Manager").exists()


class MailingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mailing
    form_class = MailingForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MessageFormset = inlineformset_factory(Mailing, Message, form=MessageForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = MessageFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = MessageFormset(instance=self.object)
        return context_data

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['clients'].queryset = Client.objects.filter(user=self.request.user)
        return form

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mailing:mailing_detail', args=[self.kwargs['pk']])

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user == self.get_object().creator or user.groups.filter(name="Manager").exists()


class MailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user == self.get_object().creator
