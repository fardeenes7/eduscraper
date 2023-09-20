from django import template
register = template.Library()
from scraper.models import Program

@register.filter
def is_saved(program, user):
    return program.is_saved(user)