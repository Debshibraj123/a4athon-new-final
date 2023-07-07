# Generated by Django 4.2.3 on 2023-07-04 13:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_alter_book_issue_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book_issue',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 12, 18, 40, 46, 818574), help_text='Date the book is due to'),
        ),
    ]
