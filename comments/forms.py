from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    comment_text = forms.CharField(label="", widget=forms.Textarea(
        attrs={'rows': 10, 'cols': 70, 'autofocus': 'True',
               'placeholder': 'Ваш комментарий'}))

    class Meta:
        model = Comment
        fields = ('comment_text',)
