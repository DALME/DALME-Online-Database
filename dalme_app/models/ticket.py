from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import options
from django.urls import reverse

from dalme_app.models.templates import dalmeIntid

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
    description = models.TextField(blank=True)
    status = models.IntegerField(choices=STATUS, default=0)
    tags = GenericRelation('Tag')
    url = models.CharField(max_length=255, blank=True)
    file = models.ForeignKey('Attachment', blank=True, null=True, on_delete=models.SET_NULL)
    comments = GenericRelation('Comment')
    assigned_to = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='ticket_assigned_to',
    )
    closing_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    closing_date = models.DateTimeField(null=True, blank=True)

    class Meta:  # noqa: D106
        ordering = ['status', 'creation_timestamp']

    def __str__(self):  # noqa: D105
        return str(self.id) + ' - ' + self.title + ' (' + self.get_status_display + ')'

    def get_absolute_url(self):
        """Return absolute url for instance."""
        return reverse('ticket_detail', kwargs={'pk': self.pk})

    @property
    def comment_count(self):
        """Return count of comments."""
        return self.comments.count()
