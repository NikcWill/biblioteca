# Generated by Django 4.2.4 on 2023-11-15 23:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bibliotecaApp', '0002_alter_livro_genery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livro',
            name='genery',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='bibliotecaApp.genero'),
        ),
        migrations.AlterField(
            model_name='livro',
            name='picture',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]