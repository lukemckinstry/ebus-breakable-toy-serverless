# Generated by Django 3.2.13 on 2022-05-13 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transit_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(db_index=True, max_length=255),
        ),
    ]