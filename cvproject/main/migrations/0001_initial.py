# Generated by Django 5.2 on 2025-05-06 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='First name')),
                ('last_name', models.CharField(max_length=50, verbose_name='Last name')),
                ('bio', models.TextField(blank=True, verbose_name='Short bio')),
                ('contacts', models.TextField(blank=True, verbose_name='Contacts (email, phone, etc.)')),
                ('skills', models.TextField(blank=True, verbose_name='Skills (comma-separated)')),
                ('projects', models.TextField(blank=True, verbose_name='Projects (comma-separated or free-form)')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
            ],
            options={
                'verbose_name': 'CV',
                'verbose_name_plural': 'CVs',
                'ordering': ['-created_at'],
            },
        ),
    ]
