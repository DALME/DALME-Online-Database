from django.contrib.auth.models import User, Group
from django.db import models
from django.urls import reverse
import django.db.models.options as options
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)


class GroupProperties(models.Model):
    """
    One-to-one extension of group model to accomodate additional group related
    data, including group types.
    """
    ADMIN = 1
    DAM = 2
    DATASET = 3
    KNOWLEDGEBASE = 4
    WEBSITE = 5
    GROUP_TYPES = (
        (ADMIN, 'Admin'),
        (DAM, 'DAM'),
        (DATASET, 'Dataset'),
        (KNOWLEDGEBASE, 'Knowledge Base'),
        (WEBSITE, 'Website')
    )

    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='properties')
    type = models.IntegerField(choices=GROUP_TYPES)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.group.name


class Profile(models.Model):
    """
    One-to-one extension of user model to accomodate additional user related
    data, including permissions of associated accounts on other platforms.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=50, blank=True)
    primary_group = models.ForeignKey(Group, to_field='id', db_index=True, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'username': self.user.username})

    @property
    def profile_image(self):
        try:
            if self.user.wagtail_userprofile.avatar is not None and self.user.wagtail_userprofile.avatar != '':
                return settings.MEDIA_URL + str(self.user.wagtail_userprofile.avatar)
            else:
                return None
        except ObjectDoesNotExist:
            return None
