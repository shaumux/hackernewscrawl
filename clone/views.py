from django.shortcuts import render
from django.views.generic import ListView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import NewsItem


# Create your views here.


class NewsItemListView(ListView):
    model = NewsItem
    context_object_name = 'news_items'
    ordering = '-id'

    def get_queryset(self):
        return NewsItem.objects.exclude(id__in=self.request.user.deleted_items.all()).order_by(self.ordering)

@csrf_exempt
def delete_post(request, id):
    if request.method=="POST":
        user = request.user
        user.deleted_items.add(id)
        return JsonResponse({
            'status':'successfully deleted'
        })

@csrf_exempt
def mark_read(request, id):
    if request.method == "POST":
        user = request.user
        user.read_items.add(id)
        return JsonResponse({
            'status': 'successfully deleted'
        })
