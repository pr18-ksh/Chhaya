# Generated by Django 5.1.3 on 2024-11-13 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Missing_persons', '0011_matchedrecord_created_at_matchedrecord_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchedrecord',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]