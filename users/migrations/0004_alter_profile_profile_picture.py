# Generated by Django 4.0.1 on 2022-01-18 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profiles/default.png', null=True, upload_to='profiles/'),
        ),
    ]
