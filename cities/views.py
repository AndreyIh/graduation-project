from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from .models import City
from .forms import CityForm



def home(request):

    cities = City.objects.all()
    paginator = Paginator(cities, 5)
    page_number = request.GET.get('page')
    cities_obj = paginator.get_page(page_number)

    return render(request, 'cities/home.html', {'objects_list': cities_obj, })


class CityDetailView(DetailView):
    queryset = City.objects.all()
    context_object_name = 'object'
    template_name = 'cities/detail.html'


class CityCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = City
    form_class = CityForm
    template_name = 'cities/create.html'
    success_url = reverse_lazy('cities:home')
    success_message = "Город %(name)s был успешно добавлен"

class CityUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = City
    form_class = CityForm
    template_name = 'cities/update.html'
    success_url = reverse_lazy('cities:home')
    success_message = "Город %(name)s был успешно изменен"


class CityDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = City
    template_name = 'cities/delete.html'
    success_url = reverse_lazy('cities:home')

    def post(self, requst, *args, **kwargs):
        messages.add_message(requst, messages.SUCCESS, 'Город был успешно удален')
        return super(CityDeleteView, self).post(requst, *args, **kwargs)

