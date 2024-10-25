# Generated by Django 5.1.2 on 2024-10-24 23:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0002_initial'),
        ('selections', '0002_initial'),
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='interview',
            options={'verbose_name': 'Интервью', 'verbose_name_plural': 'Интервью'},
        ),
        migrations.AlterModelOptions(
            name='interviewtaskitem',
            options={'verbose_name': 'Элемент задания интервью', 'verbose_name_plural': 'Элементы задания интервью'},
        ),
        migrations.AlterField(
            model_name='interview',
            name='duration',
            field=models.IntegerField(verbose_name='Продолжительность (мин)'),
        ),
        migrations.AlterField(
            model_name='interview',
            name='end_time',
            field=models.DateTimeField(verbose_name='Время окончания'),
        ),
        migrations.AlterField(
            model_name='interview',
            name='feedback',
            field=models.TextField(blank=True, null=True, verbose_name='Обратная связь'),
        ),
        migrations.AlterField(
            model_name='interview',
            name='hard_skills_rate',
            field=models.IntegerField(blank=True, null=True, verbose_name='Оценка хард скиллов'),
        ),
        migrations.AlterField(
            model_name='interview',
            name='notes',
            field=models.TextField(blank=True, null=True, verbose_name='Примечания'),
        ),
        migrations.AlterField(
            model_name='interview',
            name='recording_url',
            field=models.URLField(blank=True, null=True, verbose_name='URL записи'),
        ),
        migrations.AlterField(
            model_name='interview',
            name='result',
            field=models.CharField(choices=[('Принято', 'Принято'), ('Отклонено', 'Отклонено')], max_length=20, verbose_name='Результат'),
        ),
        migrations.AlterField(
            model_name='interview',
            name='selection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='selections.companyselection', verbose_name='Отбор'),
        ),
        migrations.AlterField(
            model_name='interview',
            name='soft_skills_rate',
            field=models.IntegerField(blank=True, null=True, verbose_name='Оценка софт скиллов'),
        ),
        migrations.AlterField(
            model_name='interview',
            name='start_time',
            field=models.DateTimeField(verbose_name='Время начала'),
        ),
        migrations.AlterField(
            model_name='interview',
            name='status',
            field=models.CharField(blank=True, choices=[('Запланировано', 'Запланировано'), ('Завершено', 'Завершено'), ('Отклонено', 'Отклонено')], max_length=20, null=True, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='interview',
            name='type',
            field=models.CharField(max_length=255, verbose_name='Тип интервью'),
        ),
        migrations.AlterField(
            model_name='interviewtaskitem',
            name='candidate_answer',
            field=models.TextField(verbose_name='Ответ кандидата'),
        ),
        migrations.AlterField(
            model_name='interviewtaskitem',
            name='interview',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interviews.interview', verbose_name='Интервью'),
        ),
        migrations.AlterField(
            model_name='interviewtaskitem',
            name='task_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.taskitem', verbose_name='Задание'),
        ),
    ]
