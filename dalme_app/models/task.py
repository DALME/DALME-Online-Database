import datetime

from django_currentuser.middleware import get_current_user

from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import options
from django.urls import reverse
from django.utils import timezone

from dalme_app.models.templates import dalmeIntid, dalmeOwned

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Task(dalmeIntid):
    """Stores information about tasks."""

    title = models.CharField(max_length=140)
    task_list = models.ForeignKey('TaskList', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    priority = models.PositiveIntegerField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(blank=True, null=True)

    # TODO: what's position?
    position = models.CharField(max_length=255, blank=True)
    url = models.CharField(max_length=255, blank=True)
    comments = GenericRelation('Comment', related_query_name='tasks')
    # TODO: doesn't creation_user cover this?
    created_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name='task_created_by',
        default=get_current_user,
    )

    # TODO: new fields
    completed_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name='completed_tasks',
    )
    files = models.ManyToManyField('Attachment', blank=True, related_name='tasks')
    resources = models.ManyToManyField('Collection', blank=True, related_name='tasks')
    assignees = models.ManyToManyField(User, blank=True, related_name='task_assignations')

    # TODO: delete these after data migration
    assigned_to = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='task_assigned_to',
    )
    file = models.ForeignKey('Attachment', blank=True, null=True, on_delete=models.SET_NULL)
    workset = models.ForeignKey('Collection', on_delete=models.PROTECT, null=True)

    class Meta:  # noqa: D106
        ordering = ['priority', 'creation_timestamp']

    def __str__(self):  # noqa: D105
        return self.title

    @property
    def comment_count(self):
        """Return count of comments."""
        return self.comments.count()

    @property
    def overdue(self):
        """Return boolean indicating whether task is overdue."""
        if self.due_date and datetime.datetime.now(tz=datetime.UTC).date() > self.due_date:
            return True
        return None

    def get_absolute_url(self):
        """Return absolute url for instance."""
        return reverse('task_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        """Save record."""
        # If Task is being marked complete, set the completed_date and completed_by
        if self.completed:
            self.completed_date = timezone.now()
            self.completed_by = get_current_user()
        super().save(*args, **kwargs)


class TaskList(dalmeIntid, dalmeOwned):
    """Stores information about task lists."""

    name = models.CharField(max_length=60)
    slug = models.SlugField(default='')
    team_link = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='team_tasklist',
        limit_choices_to={'properties__type': 3},
        null=True,
    )
    permissions = GenericRelation('Permission', related_query_name='tasklist')

    class Meta:  # noqa: D106
        ordering = ['name']
        verbose_name_plural = 'Task Lists'
        # Prevents (at the database level) creation of two lists with the same slug in the same group
        unique_together = ('team_link', 'slug')

    def __str__(self):  # noqa: D105
        return self.name

    def save(self, *args, **kwargs):
        """Save record."""
        self.slug = '_'.join(self.name.lower().split())
        super().save(*args, **kwargs)
