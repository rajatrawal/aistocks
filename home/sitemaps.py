from django.contrib import sitemaps
from django.urls import reverse


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['index', 'about_us', 'get_signals']

    def location(self, item):
        return reverse(item)
    
    

import json
with open(r'E:\rajat\Django\stock ticker\aistocks_website\static\home\stocks.json') as f:
   data = json.load(f)
   
