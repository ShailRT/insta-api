# Generated by Django 5.1.4 on 2024-12-28 08:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_profile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='followers',
            field=models.ManyToManyField(null=True, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
    ]
