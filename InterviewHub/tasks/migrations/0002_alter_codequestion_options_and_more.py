# Generated by Django 5.1.2 on 2024-10-24 23:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selections', '0003_alter_companyselection_options_and_more'),
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='codequestion',
            options={'verbose_name': 'Кодовый вопрос', 'verbose_name_plural': 'Кодовые вопросы'},
        ),
        migrations.AlterModelOptions(
            name='multiplechoicequestion',
            options={'verbose_name': 'Вопрос с выбором ответа', 'verbose_name_plural': 'Вопросы с выбором ответа'},
        ),
        migrations.AlterModelOptions(
            name='openquestion',
            options={'verbose_name': 'Открытый вопрос', 'verbose_name_plural': 'Открытые вопросы'},
        ),
        migrations.AlterModelOptions(
            name='taskitem',
            options={'verbose_name': 'Элемент задания', 'verbose_name_plural': 'Элементы задания'},
        ),
        migrations.AlterModelOptions(
            name='testtask',
            options={'verbose_name': 'Тестовое задание', 'verbose_name_plural': 'Тестовые задания'},
        ),
        migrations.AlterField(
            model_name='codequestion',
            name='code_snippet',
            field=models.TextField(verbose_name='Код'),
        ),
        migrations.AlterField(
            model_name='codequestion',
            name='is_code_run',
            field=models.BooleanField(default=False, verbose_name='Код выполнен'),
        ),
        migrations.AlterField(
            model_name='codequestion',
            name='language',
            field=models.CharField(max_length=255, verbose_name='Язык программирования'),
        ),
        migrations.AlterField(
            model_name='codequestion',
            name='task_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.taskitem', verbose_name='Элемент задания'),
        ),
        migrations.AlterField(
            model_name='multiplechoicequestion',
            name='answer_text',
            field=models.CharField(max_length=255, verbose_name='Текст ответа'),
        ),
        migrations.AlterField(
            model_name='multiplechoicequestion',
            name='is_correct_answer',
            field=models.BooleanField(verbose_name='Правильный ответ'),
        ),
        migrations.AlterField(
            model_name='multiplechoicequestion',
            name='task_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.taskitem', verbose_name='Элемент задания'),
        ),
        migrations.AlterField(
            model_name='openquestion',
            name='correct_answer',
            field=models.TextField(verbose_name='Правильный ответ'),
        ),
        migrations.AlterField(
            model_name='openquestion',
            name='task_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.taskitem', verbose_name='Элемент задания'),
        ),
        migrations.AlterField(
            model_name='taskitem',
            name='complexity',
            field=models.IntegerField(verbose_name='Сложность'),
        ),
        migrations.AlterField(
            model_name='taskitem',
            name='task_condition',
            field=models.TextField(verbose_name='Условие задания'),
        ),
        migrations.AlterField(
            model_name='taskitem',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Название задания'),
        ),
        migrations.AlterField(
            model_name='testtask',
            name='duration',
            field=models.IntegerField(verbose_name='Длительность'),
        ),
        migrations.AlterField(
            model_name='testtask',
            name='end_time',
            field=models.DateTimeField(verbose_name='Время окончания'),
        ),
        migrations.AlterField(
            model_name='testtask',
            name='recording_url',
            field=models.URLField(blank=True, null=True, verbose_name='URL записи'),
        ),
        migrations.AlterField(
            model_name='testtask',
            name='result',
            field=models.CharField(choices=[('Принято', 'Принято'), ('Отклонено', 'Отклонено')], max_length=20, verbose_name='Результат'),
        ),
        migrations.AlterField(
            model_name='testtask',
            name='selection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='selections.companyselection', verbose_name='Отбор компании'),
        ),
        migrations.AlterField(
            model_name='testtask',
            name='start_time',
            field=models.DateTimeField(verbose_name='Время начала'),
        ),
    ]
