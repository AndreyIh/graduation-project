from ckeditor.widgets import CKEditorWidget
from django import forms
from .models import Blog


class BlogForm(forms.ModelForm):
    title = forms.CharField(label='Тема', widget=forms.TextInput(
           attrs={'class': 'form-control', 'placeholder': 'Укажите тему',
                  'size': '5', 'title': 'Тема', 'autofocus': 'True'}))
    content = forms.CharField(label="", widget=CKEditorWidget(
                    attrs={'rows': 10, 'cols': 70, 'autofocus': 'True',
                           'placeholder': 'Ваш пост'}))


    class Meta(object):
        model = Blog
        fields = ('title', 'content')


class EmailBlogForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
