# Generated by Django 2.2.16 on 2022-08-03 21:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_merge_20220804_0051'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ['username'], 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]
