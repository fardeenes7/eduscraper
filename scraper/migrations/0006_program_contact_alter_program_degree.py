# Generated by Django 4.2.2 on 2023-07-04 06:34

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0005_alter_program_apply_instructions_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='contact',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='degree',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
