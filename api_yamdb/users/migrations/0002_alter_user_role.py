# Generated by Django 3.2 on 2023-03-30 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('anonym', 'anonym'), ('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin')], default='user', max_length=100, verbose_name='Роль'),
        ),
    ]
