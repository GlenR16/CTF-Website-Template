# Generated by Django 4.1.4 on 2023-02-04 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='solved_challenges',
            field=models.ManyToManyField(blank=True, null=True, to='home.challenge'),
        ),
    ]
