# Generated by Django 5.1.2 on 2024-10-16 21:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('evaluations', '0001_initial'),
        ('interviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='interviewevaluation',
            name='interview',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='interviews.interview'),
        ),
    ]
