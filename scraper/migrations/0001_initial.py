# Generated by Django 4.2.2 on 2023-07-01 13:46

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url', models.URLField()),
                ('logo', models.ImageField(blank=True, upload_to='university_logos/')),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('url', models.URLField()),
                ('details', tinymce.models.HTMLField()),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraper.university')),
            ],
        ),
    ]
