# Generated by Django 4.2.4 on 2023-11-15 22:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bibliotecaApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livro',
            name='genery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bibliotecaApp.genero'),
        ),
    ]
