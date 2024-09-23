from django.forms import ModelForm, TextInput, Textarea

from .models import News


class ArticleForm(ModelForm):
    class Meta:
        model = News
        fields = ['title', 'release', 'content']

        widgets = {
            'title': TextInput(attrs={'class': 'form-input'}),
            'release': TextInput(attrs={'class': 'form-input'}),
            'content': Textarea(attrs={'class': 'form-control'}),
        }
