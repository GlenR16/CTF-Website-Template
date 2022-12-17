# Generated by Django 4.1.4 on 2022-12-17 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_challenge_flag_alter_team_tid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='hint',
            field=models.CharField(blank=True, max_length=127, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='tid',
            field=models.CharField(default='9f609978', max_length=8, primary_key=True, serialize=False, unique=True),
        ),
    ]