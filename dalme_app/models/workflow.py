"""Model workform data."""
from django_currentuser.middleware import get_current_user

from django.conf import settings
from django.db import models
from django.db.models import options

from ida.models import ScopedBase

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Workflow(ScopedBase, models.Model):
    """Stores information about the processing workflow for records."""

    ASSESSING = 1
    PROCESSING = 2
    DONE = 3
    INGESTION = 1
    TRANSCRIPTION = 2
    MARKUP = 3
    REVIEW = 4
    PARSING = 5
    WORKFLOW_STATUS = (
        (ASSESSING, 'assessing'),
        (PROCESSING, 'processing'),
        (DONE, 'processed'),
    )
    PROCESSING_STAGES = (
        (INGESTION, 'ingestion'),
        (TRANSCRIPTION, 'transcription'),
        (MARKUP, 'markup'),
        (REVIEW, 'review'),
        (PARSING, 'parsing'),
    )

    record = models.OneToOneField('Record', on_delete=models.CASCADE, related_name='workflow', primary_key=True)
    wf_status = models.IntegerField(choices=WORKFLOW_STATUS, default=2)
    stage = models.IntegerField(choices=PROCESSING_STAGES, default=1)
    last_modified = models.DateTimeField(null=True, blank=True)
    last_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, default=get_current_user
    )
    help_flag = models.BooleanField(default=False)
    ingestion_done = models.BooleanField(default=False)
    transcription_done = models.BooleanField(default=False)
    markup_done = models.BooleanField(default=False)
    parsing_done = models.BooleanField(default=False)
    review_done = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f'Workflow: {self.record.id}'

    @property
    def status(self):
        """Return a string indicating the current status of the associated record."""
        stage_dict = dict(self.PROCESSING_STAGES)
        if 1 <= self.wf_status <= 3:  # noqa: PLR2004
            if self.wf_status != 2:  # noqa: PLR2004
                return self.get_wf_status_display()
            if getattr(self, f'{self.get_stage_display()}_done'):
                return f'awaiting {stage_dict[self.stage + 1]}'
            return f'{self.get_stage_display()} in progress'
        return 'unknown'

    @property
    def stage_done(self):
        """Return boolean indicating whether the current stage is done."""
        return getattr(self, f'{self.get_stage_display()}_done') if self.wf_status == 2 else True  # noqa: PLR2004


class WorkLog(ScopedBase, models.Model):
    """Model workflow log data."""

    id = models.AutoField(primary_key=True, unique=True, db_index=True)  # noqa: A003
    record = models.ForeignKey('Workflow', db_index=True, on_delete=models.CASCADE, related_name='work_log')
    event = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, default=get_current_user)

    def __str__(self):
        return f'{self.timestamp}: {self.record.id} ({self.user.username}) - {self.event}'
