from .models import Private_Message
from django import forms


class MessageForm(forms.ModelForm):
    message = forms.CharField(label="", widget=forms.Textarea(
        attrs={'rows': 3, 'cols': 70, 'autofocus': 'True',
               'placeholder': 'Написать сообщение...'}))

    class Meta:
        model = Private_Message
        fields = ('message',)


some_field = forms.DateField(widget=forms.TextInput(attrs={'class': 'datepicker', 'placeholder': 'mm/dd/yy'}),
                           required=False)