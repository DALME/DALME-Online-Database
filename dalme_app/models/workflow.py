from django.contrib.auth.models import User
from django.db import models
from django_currentuser.middleware import get_current_user
import django.db.models.options as options

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)


class Workflow(models.Model):
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
        (DONE, 'processed')
    )
    PROCESSING_STAGES = (
        (INGESTION, 'ingestion'),
        (TRANSCRIPTION, 'transcription'),
        (MARKUP, 'markup'),
        (REVIEW, 'review'),
        (PARSING, 'parsing')
    )

    source = models.OneToOneField('Source', on_delete=models.CASCADE, related_name='workflow', primary_key=True)
    wf_status = models.IntegerField(choices=WORKFLOW_STATUS, default=2)
    stage = models.IntegerField(choices=PROCESSING_STAGES, default=1)
    last_modified = models.DateTimeField(null=True, blank=True)
    last_user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, default=get_current_user)
    help_flag = models.BooleanField(default=False)
    ingestion_done = models.BooleanField(default=False)
    transcription_done = models.BooleanField(default=False)
    markup_done = models.BooleanField(default=False)
    parsing_done = models.BooleanField(default=False)
    review_done = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)

    @property
    def status(self):
        stage_dict = dict(self.PROCESSING_STAGES)
        if 1 <= self.wf_status <= 3:
            if self.wf_status != 2:
                return {
                    'text': self.get_wf_status_display(),
                    'tag': self.get_wf_status_display()
                    }
            else:
                if getattr(self, f'{self.get_stage_display()}_done'):
                    return {
                        'text': f'awaiting {stage_dict[self.stage + 1]}',
                        'tag': 'awaiting'
                        }
                else:
                    return {
                        'text': f'{self.get_stage_display()} in progress',
                        'tag': 'in_progress'
                        }
        else:
            return {
                'text': 'unknown',
                'tag': 'unknown'
                }

    @property
    def stage_done(self):
        if self.wf_status == 2:
            return getattr(self, f'{self.get_stage_display()}_done')
        else:
            return True


class Work_log(models.Model):
    id = models.AutoField(primary_key=True, unique=True, db_index=True)
    source = models.ForeignKey('Workflow', db_index=True, on_delete=models.CASCADE, related_name="work_log")
    event = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, default=get_current_user)
