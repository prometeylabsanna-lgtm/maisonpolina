from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    i18n = True
    alternates = True
    x_default = True

    def items(self):
        return ["core:home", "core:privacy", "core:terms"]

    def priority(self, item):
        return {"core:home": 1.0, "core:privacy": 0.3, "core:terms": 0.3}.get(
            item, 0.5
        )

    def location(self, item):
        return reverse(item)
