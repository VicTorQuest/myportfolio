from django.contrib.sitemaps import Sitemap
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy
from .models import Project

User = get_user_model()
my_user = User.objects.filter(username='Victor').first()


class PortfolioSitemap(Sitemap):
    change_freq = 'never'
    priority = 1.0
    protocol = 'https'

    def items(self):
        return [
            'index'
        ]


    def location(self, item):
        return reverse(item)

class ProjectSitemap(Sitemap):
    change_freq = 'monthly'
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Project.objects.all()

    def last_mod(self, obj):
        return obj.last_updated

class MyWorksSitemap(Sitemap):
    change_freq = 'monthly'
    priority = 0.9
    protocol = 'https'

    def items(self):
        return [
            'my_works'
        ]

    def location(self, item):
        return reverse_lazy(item).replace('%23', '#')