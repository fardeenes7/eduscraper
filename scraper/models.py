from django.db import models
from ckeditor.fields import RichTextField
from app.models import *
# Create your models here.

class University(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=200)
    logo = models.ImageField(upload_to='university_logos/', blank=True)

    class Meta:
        verbose_name_plural = "Universities"

    def __str__(self):
        return self.name
    
class Program(models.Model):
    title = models.CharField(max_length=100)
    university = models.ForeignKey(University, related_name='programs', on_delete=models.CASCADE)
    url = models.URLField(max_length=200, blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    details = RichTextField(blank=True, null=True)
    requirements = RichTextField(blank=True, null=True)
    apply_instructions = RichTextField(blank=True, null=True)
    apply_link = models.URLField(max_length=200, blank=True, null=True)
    degree = RichTextField(blank=True, null=True)
    contact = RichTextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Programs"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Program, self).save(*args, **kwargs)


    def views(self):
        if ProgramView.objects.filter(program=self).exists():
            return ProgramView.objects.filter(program=self).count()
        return 0
    
    def is_saved(self, user):
        if user.is_anonymous:
            return False
        return saved_program.objects.filter(user=user, program=self).exists()
