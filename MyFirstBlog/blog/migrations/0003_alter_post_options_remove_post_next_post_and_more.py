# Generated by Django 4.2.6 on 2023-11-12 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_next_post_post_previous_post'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_at']},
        ),
        migrations.RemoveField(
            model_name='post',
            name='next_post',
        ),
        migrations.RemoveField(
            model_name='post',
            name='previous_post',
        ),
    ]
