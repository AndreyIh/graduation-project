from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from .models import Train
from .forms import TrainForm


def home(request):

    trains = Train.objects.all()
    paginator = Paginator(trains, 5)
    page_number = request.GET.get('page')
    trains_obj = paginator.get_page(page_number)
    #meta_dict = request.META.items() 'meta_dict':meta_dict
    return render(request, 'trains/home.html', {'objects_list': trains_obj})


class TrainDetailView(DetailView):
    queryset = Train.objects.all()
    context_object_name = 'object'
    template_name = 'trains/detail.html'


class TrainCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Train
    form_class = TrainForm
    template_name = 'trains/create.html'
    success_url = reverse_lazy('trains:home')
    success_message = "Поезд № %(name)s направления %(from_city)s-%(to_city)s был успешно добавлен"


class TrainUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Train
    form_class = TrainForm
    template_name = 'trains/update.html'
    success_url = reverse_lazy('trains:home')
    success_message = "Поезд № %(name)s направления %(from_city)s-%(to_city)s был успешно изменен"


class TrainDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Train
    template_name = 'trains/delete.html'
    success_url = reverse_lazy('trains:home')

    def post(self, requst, *args, **kwargs):
        messages.add_message(requst, messages.SUCCESS, 'Маршрут был успешно удален')
        return super(TrainDeleteView, self).post(requst, *args, **kwargs)

