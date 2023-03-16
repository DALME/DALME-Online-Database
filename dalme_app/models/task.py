"""Model task data."""
from datetime import datetime

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
    task_list = models.ForeignKey('TaskList', on_delete=models.CASCADE, related_name='tasks')
    description = models.TextField(blank=True)
    priority = models.PositiveIntegerField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(blank=True, null=True)
    url = models.CharField(max_length=255, blank=True)
    comments = GenericRelation('Comment', related_query_name='tasks')
    completed_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name='completed_tasks',
    )
    files = models.ManyToManyField('Attachment', blank=True, related_name='tasks')
    resources = models.ManyToManyField('Collection', blank=True, related_name='tasks')
    assignees = models.ManyToManyField(User, blank=True, related_name='task_assignations')

    class Meta:
        ordering = ['creation_timestamp']

    def __str__(self):
        return self.title

    @property
    def comment_count(self):
        """Return count of comments."""
        return self.comments.count()

    @property
    def overdue(self):
        """Return boolean indicating whether task is overdue."""
        date = datetime.now(tz=timezone.get_current_timezone()).date()
        if self.due_date and date > self.due_date:
            return True
        return None

    def get_absolute_url(self):
        """Return absolute url for instance."""
        return reverse('task_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        """Save record."""
        # If Task is being marked complete, set the completed_date and completed_by
        if self.completed:
            date = datetime.now(tz=timezone.get_current_timezone()).date()
            self.completed_date = date
            self.completed_by = get_current_user()
        super().save(*args, **kwargs)


class TaskList(dalmeIntid, dalmeOwned):
    """Stores information about task lists."""

    name = models.CharField(max_length=60)
    slug = models.SlugField(default='')
    description = models.TextField(blank=True)
    team_link = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='team_tasklist',
        limit_choices_to={'properties__type': 3},
        null=True,
    )
    permissions = GenericRelation('Permission', related_query_name='tasklist')

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Task Lists'
        unique_together = ('name', 'team_link', 'owner')

    def __str__(self):
        return self.name

    @property
    def task_count(self):
        """Return number of tasks in list."""
        return self.tasks.count()

    def save(self, *args, **kwargs):
        """Save record."""
        self.slug = '_'.join(self.name.lower().split())
        super().save(*args, **kwargs)
