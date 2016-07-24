# django imports
import re
from django.shortcuts import render
from django.http import JsonResponse

# app imports
from .modelops import save_page_links

# 3rd party imports
import requests
from bs4 import BeautifulSoup
# Create your views here.


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
    p = parse_links(page_url, limit)


def parse_links(page_url, limit=None):
    links = []
    if is_valid_url(page_url):
        print("Fetching from: ", page_url)
        r = requests.get(page_url)
        soup = BeautifulSoup(r.text)
        for link in soup.find_all('a'):
            links.append(link.get('href'))
            if not limit:
                parse_links(link.get('href'))
            else:
                limit -= 1
                parse_links(link.get('href'), limit)
    print("links:", links)
    return links

def is_valid_url(url):
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)
