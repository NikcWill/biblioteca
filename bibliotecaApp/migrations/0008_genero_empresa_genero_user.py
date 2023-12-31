# Generated by Django 4.2.4 on 2023-12-03 00:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bibliotecaApp', '0007_remove_livro_name_sacado'),
    ]

    operations = [
        migrations.AddField(
            model_name='genero',
            name='empresa',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='empresa.empresas'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='genero',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
