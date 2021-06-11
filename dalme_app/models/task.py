import datetime
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from dalme_app.models._templates import dalmeIntid, dalmeIntidOwned
from django_currentuser.middleware import get_current_user
import django.db.models.options as options

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)


class Task(dalmeIntid):
    title = models.CharField(max_length=140)
    task_list = models.ForeignKey('TaskList', on_delete=models.CASCADE)
    due_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="task_created_by", default=get_current_user)
    assigned_to = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="task_assigned_to")
    description = models.TextField(blank=True, null=True)
    priority = models.PositiveIntegerField(blank=True, null=True)
    workset = models.ForeignKey('Set', on_delete=models.PROTECT, null=True)
    position = models.CharField(max_length=255, blank=True, default=None)
    url = models.CharField(max_length=255, null=True, default=None)
    file = models.ForeignKey('Attachment', blank=True, null=True, on_delete=models.SET_NULL)
    comments = GenericRelation('Comment', related_query_name='tasks')

    # Has due date for an instance of this object passed?
    def overdue_status(self):
        '''Returns whether the Tasks's due date has passed or not.'''
        if self.due_date and datetime.date.today() > self.due_date:
            return True

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('task_detail', kwargs={'pk': self.pk})

    # Auto-set the Task creation / completed date
    def save(self, **kwargs):
        # If Task is being marked complete, set the completed_date
        if self.completed:
            self.completed_date = timezone.now()
        super(Task, self).save()

    class Meta:
        ordering = ["priority", "creation_timestamp"]


class TaskList(dalmeIntidOwned):
    name = models.CharField(max_length=60)
    slug = models.SlugField(default="")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="task_list_group")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Task Lists"
        # Prevents (at the database level) creation of two lists with the same slug in the same group
        unique_together = ("group", "slug")

    def save(self, **kwargs):
        self.slug = '_'.join(self.name.lower().split())
        super(TaskList, self).save()
