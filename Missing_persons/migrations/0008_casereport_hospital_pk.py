# Generated by Django 5.1.3 on 2024-11-11 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Missing_persons', '0007_casereport_missing_person_pk_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='casereport',
            name='hospital_pk',
            field=models.IntegerField(blank=True, db_index=True, null=True),
        ),
    ]
