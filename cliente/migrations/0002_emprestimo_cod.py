# Generated by Django 4.2.4 on 2023-11-30 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='emprestimo',
            name='cod',
            field=models.IntegerField(default=1, unique=True),
            preserve_default=False,
        ),
    ]
