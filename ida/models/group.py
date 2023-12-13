"""Model group data."""
from django.db import models


class GroupProperties(models.Model):
    """One-to-one extension of group model.

    Accomodates additional group related data, including group types.

    We optionally scope this table to the Tenant because in some cases that
    certainly makes sense, but in other it doesn't (eg. developers). So any
    filtering must take care to correctly scope group querysets depending on
    whatever context they are in.

    """

    ADMIN = 1
    DAM = 2
    TEAM = 3
    KNOWLEDGEBASE = 4
    WEBSITE = 5
    GROUP_TYPES = (
        (ADMIN, 'Admin'),
        (DAM, 'DAM'),
        (TEAM, 'Team'),
        (KNOWLEDGEBASE, 'Knowledge Base'),
        (WEBSITE, 'Website'),
    )

    tenant = models.ForeignKey('ida.Tenant', on_delete=models.PROTECT, null=True)
    group = models.OneToOneField('auth.Group', on_delete=models.CASCADE, related_name='properties')
    group_type = models.IntegerField(choices=GROUP_TYPES)
    description = models.CharField(max_length=255)

    def __str__(self):
        if self.tenant:
            return f'{self.group.name} ({self.tenant.name})'
        return f'{self.group.name} (IDA)'
