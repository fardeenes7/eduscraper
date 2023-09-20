from django.contrib import admin
from .models import University, Program

admin.site.register(University)


class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'university', 'duration', 'degree')
    list_filter = ('university', 'duration', 'degree')
    search_fields = ('title', 'university__name', 'duration', 'degree')

admin.site.register(Program, ProgramAdmin)