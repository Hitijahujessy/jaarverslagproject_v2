# Generated by Django 5.0.2 on 2024-03-21 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_delete_codeexplainer_rename__input_chat_input_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='thread_id',
            field=models.CharField(max_length=31, null=True),
        ),
        migrations.AlterField(
            model_name='assistant',
            name='openai_id',
            field=models.CharField(default='asst_678901234567890123456789', max_length=29),
        ),
    ]
