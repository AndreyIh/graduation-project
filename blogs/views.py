from django.contrib import messages
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.db.models import Q

from .models import Blog
from .forms import BlogForm, EmailBlogForm
from comments.models import Comment


class AutorRequiredMixin1(AccessMixin):
    """Verify that the current user is author."""

    def dispatch(self, request, *args, **kwargs):
        blog = Blog.objects.filter(slug=kwargs['slug']).first()
        if not blog.author == get_user(request):
            messages.error(request, 'Изменять и удалять может только автор!')
            return redirect(f'/comments/{kwargs["slug"]}/')
        return super().dispatch(request, *args, **kwargs)


def home(request, author=None):
    if author == 'AnonymousUser' or author is None:
        blogs = Blog.objects.all()
        user_name = get_user(request).username

    else:
        blogs = Blog.objects.filter(author=get_user(request))
        user_name = get_user(request).username

    blogs_comments = []
    # Отбираем посты с комментариями сортировка идет на главной странице
    for blog in blogs:
        comments = Comment.objects.filter(blog_origin=blog)
        if len(comments) > 0:
            blogs_comments.append({'blog': blog, 'val': len(comments)})

    paginator = Paginator(blogs, 10)
    page_number = request.GET.get('page')
    blogs_obj = paginator.get_page(page_number)
    return render(request, 'blogs/home.html', {'objects_list': blogs_obj,
                                               'object_with_comments': blogs_comments,
                                               'user_name': user_name})



@login_required(login_url='/accounts/login/')
def blog_create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            blog = Blog(title=data['title'],
                        author=get_user(request),
                        content=data['content'])
            blog.save()
            messages.success(request, f'Блог {blog.title} был успешно сохранен')
            return redirect('/')
    else:
        if request.GET:
            data = request.GET
            if data:
                form = BlogForm(initial={'title': data['title'],
                                         'content': data['content']})
                return render(request, 'blogs/create.html', {'form': form})
            else:
                messages.error(request, 'Нет данных для сохранения')
                return redirect
        else:
            form = BlogForm()
            return render(request, 'blogs/create.html', {'form': form})


class BlogUpdateView(SuccessMessageMixin, LoginRequiredMixin, AutorRequiredMixin1, UpdateView):
    login_url = '/accounts/login/'
    model = Blog
    form_class = BlogForm
    template_name = 'blogs/update.html'
    success_url = reverse_lazy('home')
    success_message = "Блог %(title)s был успешно изменен"


class BlogDeleteView(SuccessMessageMixin, LoginRequiredMixin, AutorRequiredMixin1, DeleteView):
    login_url = '/accounts/login/'
    model = Blog
    template_name = 'blogs/delete.html'
    success_url = reverse_lazy('home')

    def post(self, requst, *args, **kwargs):
        messages.add_message(requst, messages.SUCCESS, 'Блог был успешно удален')
        return super(BlogDeleteView, self).post(requst, *args, **kwargs)


class SearchResultsView(ListView):
    model = Blog
    template_name = 'blogs/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Blog.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
        return object_list




def post_share(request, pk):

    blog = Blog.objects.filter(id=pk).first()
    print(blog)
    if request.method == 'POST':
        form = EmailBlogForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(blog.get_absolute_url())
            subject = f"""{cd['name']} ({cd['email']}) Советует прочесть {blog.title} """
            message = f"""Прочитай {blog.title} на {post_url}\n\n{cd['name']}\'s Комментарий: {cd['comments']}"""
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
            return render(request, 'blogs/share.html',
                          {'blog': blog, 'sent':sent})
        else:
            form = EmailBlogForm()
            return render(request, 'blogs/share.html',
                            {'blog': blog, 'form': form})
    else:
        form = EmailBlogForm()
        return render(request, 'blogs/share.html',
                      {'blog': blog, 'form': form})