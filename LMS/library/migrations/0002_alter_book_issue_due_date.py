# Generated by Django 4.2.3 on 2023-07-03 12:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book_issue',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 11, 18, 13, 40, 212678), help_text='Date the book is due to'),
        ),
    ]
