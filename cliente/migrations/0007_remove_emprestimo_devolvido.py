# Generated by Django 4.2.4 on 2023-12-02 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0006_emprestimo_dias_para_devolver'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emprestimo',
            name='devolvido',
        ),
    ]
