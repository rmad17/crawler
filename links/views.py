# django imports
from django.shortcuts import render
from django.http import JsonResponse

# app imports
from .tasks import fetch_links_task


def home(request):
    return JsonResponse({'message': 'This is a crawler'}, status=200)


def get_links(request):
    if not request.method == 'GET':
        return JsonResponse({'message': 'I swear you are upto no good'},
                            status=403)
    page_url = request.GET.get("url")
    limit = request.GET.get("limit")
    if not page_url:
        return JsonResponse({'message': 'Give me a page to crawl'},
                            status=403)
    print("url:", page_url)
    process_celery_task(page_url, limit)
    return JsonResponse({'message': 'Crawler at work...'},
                        status=200)


def process_celery_task(page_url, limit):
    results = fetch_links_task.delay(page_url)
