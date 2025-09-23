# my_portfolio/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from .models import Portfolio, Project, Service, Feedback, ProfessionalExperience, Education, Summary, Tool, ProjectCategory

CACHE_KEY = "portfolio_index_data"

def clear_portfolio_cache():
    cache.delete(CACHE_KEY)

@receiver(post_save, sender=Portfolio)
@receiver(post_delete, sender=Portfolio)
@receiver(post_save, sender=Project)
@receiver(post_delete, sender=Project)
@receiver(post_save, sender=Service)
@receiver(post_delete, sender=Service)
@receiver(post_save, sender=Feedback)
@receiver(post_delete, sender=Feedback)
@receiver(post_save, sender=ProfessionalExperience)
@receiver(post_delete, sender=ProfessionalExperience)
@receiver(post_save, sender=Education)
@receiver(post_delete, sender=Education)
@receiver(post_save, sender=Summary)
@receiver(post_delete, sender=Summary)
@receiver(post_save, sender=Tool)
@receiver(post_delete, sender=Tool)
@receiver(post_save, sender=ProjectCategory)
@receiver(post_delete, sender=ProjectCategory)
def clear_cache_on_change(sender, **kwargs):
    clear_portfolio_cache()
