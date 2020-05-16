from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import RouteForm, RouteModelForm, Route
from django.contrib import messages
from trains.models import Train
from django.views.generic import DetailView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

def dfs_paths(graph, start, goal):
    """Функция поиска всех возможных маршрутов
    из одного города в другой. Вариант посещения
    одного и того же города более одного раза,
    не рассматривается.
    """
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == goal:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_]))

def get_graph():
    qs = Train.objects.values('from_city')
    from_city_set = set(i['from_city'] for i in qs)
    graph = {}
    for city in from_city_set:
        trains = Train.objects.filter(from_city=city).values('to_city')
        tmp = set(i['to_city'] for i in trains)
        graph[city] = tmp
    return graph




#@login_required(login_url='/login/')
def travel (request):
    form = RouteForm()
    return render(request, 'routes/home.html', {'form': form})


def find_routes(request):
    if request.method == "POST":
        form = RouteForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            # assert False
            from_city = data['from_city']
            to_city = data['to_city']
            cities = data['cities']
            travelling_time = data['travelling_time']
            graph = get_graph()
            all_ways = list(dfs_paths(graph, from_city.id, to_city.id))
            if len(all_ways) == 0:
                messages.error(request, 'Маршрутов удовлетворяющих условиям не существует')
                return render(request, 'routes/home.html', {'form': form})
            if cities:
                cities = [city.id for city in cities]
                right_ways = []
                for way in all_ways:
                    if all(point in way for point in cities):
                        right_ways.append(way)
                if not right_ways:
                    messages.error(request, 'Маршрутов через эти города не возможен')
                    return render(request, 'routes/home.html', {'form': form})
            else:
                right_ways = all_ways

            trains = []
            for route in right_ways:
                # для городов по пути следования, выбираем необходимые поезда
                tmp = {}
                tmp['trains'] = []
                total_time = 0
                for index in range(len(route) - 1):
                    qs = Train.objects.filter(
                        from_city=route[index], to_city=route[index + 1])
                    qs = qs.order_by('travel_time').first()
                    total_time += qs.travel_time
                    tmp['trains'].append(qs)
                tmp['total_time'] = total_time
                if total_time <= travelling_time:
                    # если общее время в пути, меньще заданного,
                    # то добавляем маршрут в общий список
                    trains.append(tmp)
            if not trains:
                # если список пуст, то нет таких маршрутов,
                # которые удовлетворяли бы заданным условиям
                messages.error(request, 'Время в пути маршрута(ов), больше заданного.')
                return render(request, 'routes/home.html', {'form': form})
            routes = []
            cities = {'from_city': from_city.name, 'to_city': to_city.name}
            for tr in trains:
            # формирую список всех маршрутов
                routes.append({'route': tr['trains'],
                                'total_time': tr['total_time'],
                                'from_city': from_city.name,
                                'to_city': to_city.name})
            sorted_routes = []
            if len(routes) == 1:
                sorted_routes = routes
            else:
                # если маршрутов больше одного, то сортирую их по времени
                times = list(set(x['total_time'] for x in routes))
                times = sorted(times)
                for time in times:
                    for route in routes:
                        if time == route['total_time']:
                            sorted_routes.append(route)

            context = {}
            form = RouteForm()
            context['form'] = form
            context['routes'] = sorted_routes
            context['cities'] = cities
            return render(request, 'routes/home.html', context)

        return render(request, 'routes/home.html', {'form': form})
    else:
        messages.error(request, 'Создайте маршрут')
        form = RouteForm()
        return render(request, 'routes/home.html', {'form': form})

def add_route(request):
    if request.method == 'POST':
        form = RouteModelForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            name = data['name']
            travel_times = data['travel_times']
            from_city = data['from_city']
            to_city = data['to_city']
            train_list = data['trains'].replace('  ', ' ').strip()
            qs = Train.objects.filter(id__in=train_list.split())
            route = Route(name = name, from_city=from_city,
                          to_city=to_city, travel_times=travel_times)
            route.save()
            for tr in qs:
                route.trains.add(tr.id)
            messages.success(request, f'Маршрут {name} был успешно сохранен')
            return redirect('/')
    else:
        data = request.GET
        if data:
            travel_times = data['travel_times']
            from_city = data['from_city']
            to_city = data['to_city']
            train_list = data['trains'].replace('  ', ' ').strip()
            qs = Train.objects.filter(id__in=train_list.split())

            form = RouteModelForm(initial={'from_city':from_city,
                                           'to_city':to_city,
                                           'travel_times':travel_times,
                                           'trains':train_list})
            route_desc = []
            for tr in qs:
                dsc = f'Поезд № {tr.name} следующий из г.{tr.from_city} ' \
                      f'в г.{tr.from_city} Время в пути {tr.travel_time}.'
                route_desc.append(dsc)
            context = {'form': form, 'descr':route_desc, 'from_city': from_city,
                       'to_city':to_city, 'travel_times': travel_times}
            return render(request,'routes/create.html', context)

        else:
            messages.error(request, 'Нет данных для сохранения')
            return redirect

class RouteDetailView(DetailView):
    queryset = Route.objects.all()
    context_object_name = 'object'
    template_name = 'routes/detail.html'

class RouteListView(ListView):
    queryset = Route.objects.all()
    context_object_name = 'objects_list'
    template_name = 'routes/list.html'

class RouteDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Route
    template_name = 'routes/delete.html'
    success_url = reverse_lazy('home')

    def post(self, requst, *args, **kwargs):
        messages.add_message(requst, messages.SUCCESS, 'Маршрут был успешно удален')
        return super(RouteDeleteView, self).post(requst, *args, **kwargs)
