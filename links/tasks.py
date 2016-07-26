# -*- coding: utf-8 -*-
#
# Copyright © 2016 rmad
#
# Distributed under terms of the MIT license.

"""
Tasks for celery
"""
# django imports
import re

# app imports
from celery.decorators import task
from .modelops import save_page_links

# 3rd party imports
import requests
from bs4 import BeautifulSoup


@task(name="fetch_links_task")
def fetch_links_task(page_url):
    links = []
    print("Fetching from: ", page_url)
    r = requests.get(page_url)
    soup = BeautifulSoup(r.text)
    for link in soup.find_all('a'):
        if is_valid_url(link.get('href')):
            links.append(link.get('href'))
    dbop = save_page_links(page_url, links)
    print("dbop:", dbop)
    return links


def is_valid_url(url):
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain... # noqa
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)
