from __future__ import absolute_import

from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    def items(self):
        return ["home", "about"]  # , 'contact', 't&c', 'policies', 'cookies']

    def location(self, item):
        return reverse(item)
