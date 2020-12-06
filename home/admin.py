from django.contrib import admin
from django.contrib.auth.models import Group
from . import models

admin.site.site_header = 'Issue Tracker'
admin.site.site_title = 'Issue Tracker'
admin.site.index_title = 'Admin Dashboard'
admin.site.unregister(Group)
admin.site.register(models.Project)
admin.site.register(models.Ticket)


admin.site.register(models.TicketType)
admin.site.register(models.TicketPriority)
admin.site.register(models.TicketStatus)
admin.site.register(models.TicketHistory)
admin.site.register(models.TicketComment)
