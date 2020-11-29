from django.contrib.auth.models import Group
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from dalme_app.models._templates import dalmeBasic, dalmeUuidOwned
import django.db.models.options as options
import uuid
from collections import Counter
from dalme_app.models.reference import LanguageReference

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)


class Set(dalmeUuidOwned):
    CORPUS = 1  # a set representing a coherent body of materials defined by a project or sub-project
    COLLECTION = 2  # a generic set defined by a user for any purpose -- collections could potentially by qualified by other terms
    DATASET = 3  # a set corresponding to a project or sub-project and related to a team user group
    WORKSET = 4  # a set defined as part of a project's workflow for the purpose of systematically performing a well-defined task to its members
    PRIVATE = 1  # only owner can view set
    VIEW = 2  # others can view the set
    ADD = 3  # others can view the set and add members
    DELETE = 4  # others can view the set and add and delete members
    SET_TYPES = (
        (CORPUS, 'Corpus'),
        (COLLECTION, 'Collection'),
        (DATASET, 'Dataset'),
        (WORKSET, 'Workset')
    )
    PERMISSIONS = [
        (PRIVATE, 'Private'),
        (VIEW, 'Others: view'),
        (ADD, 'Others: view|add'),
        (DELETE, 'Others: view|add|delete')
    ]

    name = models.CharField(max_length=255)
    set_type = models.IntegerField(choices=SET_TYPES)
    is_public = models.BooleanField(default=False)
    has_landing = models.BooleanField(default=False)
    endpoint = models.CharField(max_length=55)
    permissions = models.IntegerField(choices=PERMISSIONS, default=VIEW)
    description = models.TextField()
    comments = GenericRelation('Comment')
    stat_title = models.CharField(max_length=25, null=True, blank=True)
    stat_text = models.CharField(max_length=255, null=True, blank=True)
    dataset_usergroup = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='dataset', limit_choices_to={'properties__type': 3}, null=True)

    def __str__(self):
        return f'{self.name} ({self.set_type})'

    def get_absolute_url(self):
        return reverse('set_detail', kwargs={'pk': self.id})

    @property
    def workset_progress(self):
        done = self.members.filter(workset_done=True).count()
        total = self.members.count()
        if total != 0:
            return done * 100 / total
        else:
            return 0

    @property
    def detail_string(self):
        result = self.get_set_type_display() if not self.is_public else 'Public ' + self.get_set_type_display()
        result = result + ' | {}'.format(self.dataset_usergroup.name) if self.set_type == 3 else result + ' | {}'.format(self.owner.profile.full_name)
        result = result + ' | {} members'.format(self.member_count)
        return result

    @property
    def member_count(self):
        return self.members.count()

    def get_public_member_count(self):
        return self.members.filter(source__workflow__is_public=True).count()

    def get_languages(self):
        return [[LanguageReference.objects.get(pk=i).name, i] for i in set(self.members.filter(source__attributes__attribute_type=15).values_list('source__attributes__value_JSON__id', flat=True))]

    def get_public_languages(self):
        return [[LanguageReference.objects.get(pk=i).name, i] for i in set(self.members.filter(source__attributes__attribute_type=15, source__workflow__is_public=True).values_list('source__attributes__value_JSON__id', flat=True))]

    def get_time_coverage(self):
        years = self.members.filter(source__attributes__attribute_type__in=[19, 25, 26]).order_by('source__attributes__value_DATE_y').values_list('source__attributes__value_DATE_y', flat=True)
        return dict(Counter(years))

    def get_public_time_coverage(self):
        years = self.members.filter(source__attributes__attribute_type__in=[19, 25, 26], source__workflow__is_public=True).order_by('source__attributes__value_DATE_y').values_list('source__attributes__value_DATE_y', flat=True)
        return dict(Counter(years))


class Set_x_content(dalmeBasic):
    set_id = models.ForeignKey(Set, on_delete=models.CASCADE, related_name='members')
    content_object = GenericForeignKey('content_type', 'object_id')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.UUIDField(default=uuid.uuid4, db_index=True)
    workset_done = models.BooleanField(default=False)

    class Meta:
        unique_together = ('content_type', 'object_id', 'set_id')
        ordering = ['set_id', 'id']
