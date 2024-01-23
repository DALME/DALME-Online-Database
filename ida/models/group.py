"""Model group data."""
from django.db import models

from ida.tenant import get_current_tenant

DESCRIPTION_MAX_LENGTH = 255


class GroupProperties(models.Model):
    """One-to-one extension of group model.

    Accomodates additional group related data, including group types.

    We allow the optional scoping of rows on this table to some Tenant because
    in some cases, for certain groups, that certainly makes sense. But in
    others it doesn't (for example a 'developers' group would need to be
    'trans-tenant'). So, any filtering that happens must take care to correctly
    scope group querysets depending on whatever context it's in.

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
    description = models.CharField(max_length=DESCRIPTION_MAX_LENGTH)

    def __str__(self):
        suffix = self.group.properties.tenant.name if self.tenant else 'IDA'
        return f'{self.group.name} ({suffix})'

    def save(self, *args, **kwargs):
        """Override the save method to populate additional GroupProperties data.

        We do this here rather than in a signal because we want to make sure
        the process is atomic (which is indeed true within save but not for a
        signal, by default).

        """
        created = self._state.adding
        if created:
            tenant = get_current_tenant()
            if bool(tenant):  # This just checks the proxy is actually bound to a value.
                self.tenant = tenant
        super().save(*args, **kwargs)
