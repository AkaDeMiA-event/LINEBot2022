# Generated by Django 4.0 on 2022-02-25 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('numeron', '0002_remove_numeron_number_numeron_number_str'),
    ]

    operations = [
        migrations.AddField(
            model_name='numeron',
            name='line_id',
            field=models.CharField(default='あ', max_length=150),
            preserve_default=False,
        ),
    ]
