#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
foursquare category
fetch all category name list foursquare api
"""
__author__ = 'Yoshiya Ito <myon53@gmail.com>'
__version__ = '0.0.1'
__date__ = '2016-12-14'
import requests
import csv

URL = 'https://api.foursquare.com/v2/venues/categories?oauth_token=X3UNPQ1J2NZLVT5NNQQ5MWX2ITTFJXUV2MVLWGCZCBUWLJKU&v=20161214'
ID = '4d4b7105d754a06374d81259'

def fetch_category(categories, parent):
    """ recursive fetch category
    Yield:
        - category_id
        - category_name
        - parent_category_name
    """
    for category in categories:
        if len(category['categories']) == 0:
            yield category['id'], category['name'], parent
        else:
            yield from fetch_category(category['categories'], category['name'])


if __name__ == '__main__':
    r = requests.get(URL, headers={'Accept-Language': 'ja'}).json()
    categories = [category['categories'] for category in r['response']['categories'] if category['id'] == ID]
    with open('categories.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(['ID', 'カテゴリー名', '親カテゴリー'])
        for id, category, parent in fetch_category(categories[0], None):
            writer.writerow([id, category, parent or ''])
