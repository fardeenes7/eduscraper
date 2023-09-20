from django.db import models
from django.contrib.auth.models import User
# from scraper.models import  Program

class saved_program(models.Model):
    user = models.ForeignKey(User,related_name='saved_programs', on_delete=models.CASCADE)
    program = models.ForeignKey('scraper.Program',related_name='saved_programs', on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.program.title} saved by {self.user.username}'
    

class ProgramView(models.Model):
    user = models.ForeignKey(User,related_name='program_views', on_delete=models.SET_NULL, null=True, blank=True)
    program = models.ForeignKey('scraper.Program',related_name='program_views', on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.program.title} viewed by {self.user.username}'