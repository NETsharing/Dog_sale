# Generated by Django 2.2.5 on 2019-11-20 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20191120_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=models.TextField(blank=True, null=True, verbose_name='Текст объявления'),
        ),
    ]
