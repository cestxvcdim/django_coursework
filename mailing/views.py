from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'mailing/home.html'


@login_required
def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'name: {name}\nphone: {phone}\nmessage: {message}')
    return render(request, 'mailing/contacts.html')
