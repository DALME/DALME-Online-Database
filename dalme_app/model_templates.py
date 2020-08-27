"""
This file contains templates for models, used in dalme_app.models. These templates
are used to more easily associate common data points with those models, things like
timestamps and unique IDs.
"""
from django.db import models
from django.contrib.auth.models import User
#from dalme_app.utils import get_current_user
import uuid
from threading import local

_user = local()


def get_current_username():
    return _user.__getattribute__('username')


def get_current_user():
    return _user.__getattribute__('user')


class dalmeBasic(models.Model):
    """ Model template with timestamps, but no pre-defined ID """
    creation_user = models.ForeignKey(User, on_delete=models.SET_NULL, default=get_current_user, related_name="%(app_label)s_%(class)s_creation", null=True)
    creation_timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modification_user = models.ForeignKey(User, on_delete=models.SET_NULL, default=get_current_user, related_name="%(app_label)s_%(class)s_modification", null=True)
    modification_timestamp = models.DateTimeField(auto_now=True, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="%(app_label)s_%(class)s_related", null=True)

    def class_name(self):
        return self.__class__.__name__

    def save(self, *args, **kwargs):
        if self._state.adding is True:
            self.owner = get_current_user()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class dalmeUuid(models.Model):
    """ Model template with a unique ID assigned by `uuid.uuid4`, resulting in a long, random identifier. """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    creation_user = models.ForeignKey(User, on_delete=models.SET_NULL, default=get_current_user, related_name="%(app_label)s_%(class)s_creation", null=True)
    creation_timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modification_user = models.ForeignKey(User, on_delete=models.SET_NULL, default=get_current_user, related_name="%(app_label)s_%(class)s_modification", null=True)
    modification_timestamp = models.DateTimeField(auto_now=True, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="%(app_label)s_%(class)s_related", null=True)

    def class_name(self):
        return self.__class__.__name__

    def save(self, *args, **kwargs):
        if self._state.adding is True:
            self.owner = get_current_user()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class dalmeIntid(models.Model):
    """ Model template with a unique ID assigned as a sequential integer """
    id = models.AutoField(primary_key=True, unique=True, db_index=True)
    creation_user = models.ForeignKey(User, on_delete=models.SET_NULL, default=get_current_user, related_name="%(app_label)s_%(class)s_creation", null=True)
    creation_timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modification_user = models.ForeignKey(User, on_delete=models.SET_NULL, default=get_current_user, related_name="%(app_label)s_%(class)s_modification", null=True)
    modification_timestamp = models.DateTimeField(auto_now=True, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="%(app_label)s_%(class)s_related", null=True)

    def class_name(self):
        return self.__class__.__name__

    def save(self, *args, **kwargs):
        if self._state.adding is True:
            self.owner = get_current_user()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
