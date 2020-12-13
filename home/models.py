from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    # Project model
    title = models.CharField(max_length=20)
    description = models.TextField()
    archived = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    manager = models.ForeignKey(
        User, related_name='manager', on_delete=models.CASCADE)
    developers = models.ManyToManyField(User, related_name='developers')

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.title


class TicketPriority(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()

    class Meta:
        verbose_name = 'Ticket Priority'
        verbose_name_plural = 'Ticket Priorities'

    def __str__(self):
        return self.name


class TicketStatus(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()

    class Meta:
        verbose_name = 'Ticket Status'
        verbose_name_plural = 'Ticket Statuses'

    def __str__(self):
        return self.name


class TicketType(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()

    class Meta:
        verbose_name = 'Ticket Type'
        verbose_name_plural = 'Ticket Types'

    def __str__(self):
        return self.name


class Ticket(models.Model):
    # Represents issues raised
    ticket_type = models.ForeignKey(
        TicketType, on_delete=models.SET_NULL, null=True)
    ticket_priority = models.ForeignKey(
        TicketPriority, on_delete=models.SET_NULL, null=True)
    ticket_status = models.ForeignKey(
        TicketStatus, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=20)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    # TODO: change this to soft delete
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ticket_owner')
    assigned_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='assigned_to_developer', blank=True, null=True)
    archived = models.BooleanField()

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

    def __str__(self):
        return self.title


class TicketAttachment(models.Model):
    ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    description = models.TextField()
    attachment_url = models.URLField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ticket Attachment'
        verbose_name_plural = 'Ticket Attachments'


class TicketComment(models.Model):
    ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ticket Comment'
        verbose_name_plural = 'Ticket Comments'

    def __str__(self):
        return self.comment


class TicketHistory(models.Model):
    ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.CharField(max_length=20)
    old_value = models.TextField()
    new_value = models.TextField()

    class Meta:
        verbose_name = 'Ticket History'
        verbose_name_plural = 'Ticket Histories'

    def __str__(self):
        return str(self.ticket_id) + ' <-> ' + str(self.user_id)


class TicketNotification(models.Model):
    ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    recipient_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipient_id')
    sender_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sender_id')
    created = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=30)
    body = models.TextField()
    is_read = models.BooleanField()

    class Meta:
        verbose_name = 'Ticket Notification'
        verbose_name_plural = 'Ticket Notifications'

    def __str__(self):
        return self.subject
