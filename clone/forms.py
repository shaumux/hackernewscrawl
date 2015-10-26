from django.forms import ModelForm
from .models import NewsItem


class NewsItemForm(ModelForm):
    class Meta:
        model = NewsItem
        exclude = ('created_on', 'updated_on')