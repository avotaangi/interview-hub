# Generated by Django 5.1.2 on 2024-10-24 22:56

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluations', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='interviewevaluation',
            name='evaluation_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testevaluation',
            name='evaluation_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
