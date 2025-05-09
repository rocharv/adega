# Generated by Django 5.2 on 2025-05-07 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category_manager', '0002_alter_category_upc'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_fungible',
            field=models.BooleanField(default=False, help_text='Marque se os itens criados a partir dessa categoria não atributos de controle individual como etiqueta de patrimônio ou número de série. Exemplo: papel, caneta, etc.', verbose_name='Fungível'),
        ),
    ]
