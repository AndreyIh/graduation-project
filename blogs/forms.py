from ckeditor.widgets import CKEditorWidget
from django import forms
from taggit.forms import TagField

from .models import Blog

STATUS_CHOICES = (
    ('проект', 'Проект'),
    ('финал', 'Финал'),
)


class BlogForm(forms.ModelForm):
    title = forms.CharField(label='Тема', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Укажите тему',
               'size': '5', 'title': 'Тема', 'autofocus': 'True'}))
    content = forms.CharField(label="", widget=CKEditorWidget(
        attrs={'rows': 10, 'cols': 70, 'autofocus': 'True',
               'placeholder': 'Ваш пост'}))
    status = forms.CharField(max_length=50,
                             widget=forms.Select(choices=STATUS_CHOICES), )
    tags = TagField()

    class Meta(object):
        model = Blog
        fields = ('title', 'content', 'status', 'tags')


class EmailBlogForm(forms.Form):
    to = forms.EmailField(label='С кем вы хотите поделиться', initial='example@mail.com')
    comments = forms.CharField(required=False, label='Ваш комметарий', widget=forms.Textarea(attrs={'rows': 3}))
