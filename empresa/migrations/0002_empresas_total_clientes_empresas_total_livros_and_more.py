# Generated by Django 4.2.4 on 2023-12-03 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresas',
            name='total_clientes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='empresas',
            name='total_livros',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='empresas',
            name='total_livros_emprestados',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='empresas',
            name='total_usuarios',
            field=models.IntegerField(default=0),
        ),
    ]
