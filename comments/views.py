from django.contrib import messages
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Count

from blogs.models import Blog
from .models import Comment
from .forms import CommentForm


def sorting_comments(comments):
    """ сортирует выборку комментариев в соответствии порядка вывода, с учетов веток"""
    dict_view, a = {}, []
    for element in comments:
        if dict_view.get(element.comment_origin):
            dict_view[element.comment_origin].append(element.id)
        else:
            dict_view[element.comment_origin] = [element.id]
    if len(dict_view) > 0:
        for i in dict_view.keys():
            if i == 0:
                a = dict_view.get(0)
            else:
                if i in a:
                    a = a[:a.index(i) + 1] + dict_view.get(i) + a[a.index(i) + 1:]
        new_comments = []
        for i in a:
            temp = comments
            new_comments.append(temp.filter(id=i).first())
        return new_comments
    new_comments = []
    return new_comments


def comment_view(request, slug, year, month, day):
    blog = Blog.objects.filter(slug=slug, create_time__year=year, create_time__month=month, create_time__day=day).first()
    comments = Comment.objects.filter(blog_origin=blog)
    comments = sorting_comments(comments)
    for comment in comments:
        comment.lvl = 100 - comment.lvl * 25
    # Формирование списка похожих статей.
    post_tags_ids = blog.tags.values_list('id', flat=True)
    similar_posts = Blog.objects.filter(tags__in=post_tags_ids).exclude(id=blog.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')) \
                        .order_by('-same_tags', '-create_time')[:4]

    return render(request, 'blogs/detail.html', {'object': blog, 'comments': comments,
                                                 'similar_posts': similar_posts})


@login_required(login_url='/accounts/login/')
def add_answer_comment(request, pk_b, pk_c):
    """ Добавления комментария, как к посту, так и ответы на другие комментарии"""
    blog = Blog.objects.filter(pk=pk_b).first()
    comment = Comment.objects.filter(pk=pk_c).first()
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            if pk_c == 0:
                lvl = 0
                comment_id = 0
            else:
                lvl = 3 if comment.lvl >= 3 else (comment.lvl + 1)
                comment_id = comment.id
            comment = Comment(blog_origin=blog,
                              comment_text=data['comment_text'],
                              author=get_user(request),
                              comment_origin=comment_id,
                              lvl=lvl)
            comment.save()
            messages.success(request, f'Комментарий был успешно добавлен')
            return redirect(f'/comments/{blog.create_time.year}/{blog.create_time.month}/{blog.create_time.day}/{blog.slug}/')


    else:

        return render(request, 'comments/comments.html', {'object': blog, 'comment': comment, 'form': form})
