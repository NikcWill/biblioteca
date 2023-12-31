# Generated by Django 4.2.4 on 2023-11-15 22:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Gênero',
                'verbose_name_plural': 'Gêneros',
            },
        ),
        migrations.CreateModel(
            name='Livro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=255)),
                ('pg', models.IntegerField()),
                ('picture', models.ImageField(upload_to='')),
                ('author', models.CharField(max_length=255)),
                ('qtd', models.IntegerField()),
                ('name_sacado', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField()),
                ('in_stock', models.BooleanField(default=False)),
                ('genery', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='bibliotecaApp.genero')),
            ],
            options={
                'verbose_name': 'Livro',
                'verbose_name_plural': 'Livros',
            },
        ),
    ]
