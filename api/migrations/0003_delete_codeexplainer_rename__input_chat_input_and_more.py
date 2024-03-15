# Generated by Django 5.0.2 on 2024-03-15 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_assistant_files'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CodeExplainer',
        ),
        migrations.RenameField(
            model_name='chat',
            old_name='_input',
            new_name='input',
        ),
        migrations.RenameField(
            model_name='chat',
            old_name='_output',
            new_name='output',
        ),
        migrations.AddField(
            model_name='assistant',
            name='openai_id',
            field=models.CharField(default='asst_67890123456789012345', max_length=25),
        ),
        migrations.DeleteModel(
            name='UploadedFile',
        ),
    ]