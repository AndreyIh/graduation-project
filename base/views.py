# from ckeditor.widgets import LazyEncoder
# from django.core.serializers import serialize
# messages = serialize('json', messages, cls=LazyEncoder)
from django.shortcuts import render


def resume(request):
    return render(request, 'resume.html', )



