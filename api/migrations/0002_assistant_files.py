# Generated by Django 5.0.2 on 2024-03-13 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assistant',
            name='files',
            field=models.FileField(blank=True, null=True, upload_to='assistant_files/'),
        ),
    ]
