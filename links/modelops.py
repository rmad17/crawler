# -*- coding: utf-8 -*-
#
# Copyright © 2016 rmad
# Distributed under terms of the MIT license.

"""
Model Operations are performed here.
"""
from .models import PageData


def save_page_links(page_url, page_links):
    if not page_links:
        return None
    page_data = PageData(page_url=page_url, page_links=page_links)
    page_data.save()
    return page_data
