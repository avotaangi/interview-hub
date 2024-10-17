# Generated by Django 5.1.2 on 2024-10-16 21:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('selections', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('complexity', models.IntegerField()),
                ('task_condition', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='OpenQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct_answer', models.TextField()),
                ('task_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.taskitem')),
            ],
        ),
        migrations.CreateModel(
            name='MultipleChoiceQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.CharField(max_length=255)),
                ('is_correct_answer', models.BooleanField()),
                ('task_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.taskitem')),
            ],
        ),
        migrations.CreateModel(
            name='CodeQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=255)),
                ('is_code_run', models.BooleanField(default=False)),
                ('code_snippet', models.TextField()),
                ('task_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.taskitem')),
            ],
        ),
        migrations.CreateModel(
            name='TestTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('duration', models.IntegerField()),
                ('result', models.CharField(choices=[('Принято', 'Принято'), ('Отклонено', 'Отклонено')], max_length=20)),
                ('recording_url', models.URLField(blank=True, null=True)),
                ('selection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='selections.companyselection')),
            ],
        ),
    ]
