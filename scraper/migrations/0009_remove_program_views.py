# Generated by Django 4.2.2 on 2023-08-18 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0008_alter_program_university'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='program',
            name='views',
        ),
    ]