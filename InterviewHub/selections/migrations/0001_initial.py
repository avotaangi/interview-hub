# Generated by Django 5.1.2 on 2024-10-16 21:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('companies', '0001_initial'),
        ('resumes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestTaskItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('candidate_answer', models.TextField()),
                ('interviewer_comment', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CompanySelection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('На рассмотрении', 'На рассмотрении'), ('Принят', 'Принят'), ('Отклонен', 'Отклонен')], max_length=20)),
                ('interviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.interviewer')),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumes.resume')),
            ],
        ),
    ]
