# Generated by Django 5.1 on 2024-08-11 05:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producto',
            old_name='categoriaId',
            new_name='categoria',
        ),
        migrations.RenameField(
            model_name='producto',
            old_name='unidadesId',
            new_name='unidad',
        ),
    ]
