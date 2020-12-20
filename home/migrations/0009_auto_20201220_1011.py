# Generated by Django 3.1.3 on 2020-12-20 10:11

from django.db import migrations


class Migration(migrations.Migration):

    def add_ticket_types(apps, schema_editor):
        TicketType = apps.get_model('home', 'TicketType')
        type = TicketType(
            name='Error report',
            description='Report a bug or a problem'
        )
        type.save()
        type = TicketType(
            name='Feature request',
            description='Request a new functionality'
        )
        type.save()
        type = TicketType(
            name='Service request',
            description='Request for help'
        )
        type.save()

    dependencies = [
        ('home', '0008_auto_20201220_0752'),
    ]

    operations = [
        migrations.RunPython(add_ticket_types)
    ]
