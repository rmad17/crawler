# -*- coding: utf-8 -*-
#
# Copyright © 2016 rmad
# Distributed under terms of the MIT license.

"""
Model Operations are performed here.
"""
from .models import PageData
from django.db import IntegrityError


def save_page_links(page_url, page_links):
    if not page_links:
        return None
    try:
        page_data = PageData(page_url=page_url, page_links=page_links)
        page_data.save()
        return page_data
    except IntegrityError as e:
        return e.__cause__


def get_page_link_by_page_url(url):
    return PageData.objects.filter(page_url=url).exists()
