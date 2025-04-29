"""Analytics mixin."""

import json
from contextlib import suppress
from datetime import UTC, datetime, timedelta

import requests
from requests.exceptions import ConnectTimeout

from django.conf import settings
from django.db import models


class AnalyticsMixin(models.Model):
    analytics_data = models.JSONField(null=True, blank=True)
    analytics_updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def update_analytics(self):
        target = f'/features/{self.slug}/'
        query = {
            'site_id': 'dalme.org',
            'metrics': settings.PLAUSIBLE_METRICS,
            'date_range': 'all',
            'filters': [['is', 'event:page', [target]]],
        }

        with suppress(ConnectTimeout):
            response = requests.post(
                settings.PLAUSIBLE_API_URL,
                headers={
                    'Authorization': f'Bearer {settings.PLAUSIBLE_API_KEY}',
                    'Content-type': 'application/json',
                },
                data=json.dumps(query),
                timeout=1,
            )
            data = json.loads(response.content)
            metrics = data.get('results')[0].get('metrics')
            self.analytics_data = {m: metrics[i] for i, m in enumerate(settings.PLAUSIBLE_METRICS)}
            self.analytics_updated_at = datetime.now(tz=UTC)
            self.save(update_fields=['analytics_data', 'analytics_updated_at'])

    @property
    def analytics_is_stale(self):
        return (
            self.analytics_data is None
            or self.analytics_updated_at is None
            or self.analytics_updated_at < datetime.now(tz=UTC) - timedelta(days=settings.PLAUSIBLE_UPDATE_INTERVAL)
        )

    @property
    def analytics(self):
        try:
            if self.analytics_is_stale:
                self.update_analytics()
            return self.analytics_data  # noqa: TRY300
        except:  # noqa: E722
            return None
