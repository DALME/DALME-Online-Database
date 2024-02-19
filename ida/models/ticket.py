"""Model ticket data."""
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import options
from django.urls import reverse

from ida.models.templates import dalmeIntid

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Ticket(dalmeIntid):
    """Stores information about tickets."""

    OPEN = 0
    CLOSED = 1
    STATUS = (
        (OPEN, 'Open'),
        (CLOSED, 'Closed'),
    )

    subject = models.CharField(max_length=140)
    description = models.TextField(blank=True, null=True)
    status = models.IntegerField(choices=STATUS, default=0)
    url = models.CharField(max_length=255, blank=True, null=True)
    files = models.ManyToManyField('dalme_app.Attachment', blank=True, related_name='tickets')
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='ticket_assigned_to',
    )
    closing_user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    closing_date = models.DateTimeField(null=True, blank=True)
    tags = GenericRelation('dalme_app.Tag')
    comments = GenericRelation('dalme_app.Comment')

    class Meta:
        ordering = ['status', 'creation_timestamp']

    def __str__(self):
        return str(self.id) + ' - ' + self.title + ' (' + self.get_status_display + ')'

    def get_absolute_url(self):
        """Return absolute url for instance."""
        return reverse('ticket_detail', kwargs={'pk': self.pk})

    @property
    def comment_count(self):
        """Return count of comments."""
        return self.comments.count()
