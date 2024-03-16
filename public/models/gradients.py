"""Model gradient data."""

from django.db import models


class Gradient(models.Model):
    id = models.AutoField(primary_key=True, unique=True, db_index=True)
    colour_1 = models.CharField(max_length=9)
    colour_2 = models.CharField(max_length=9)
    angle = models.CharField(max_length=3)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.css

    @property
    def css(self):
        return f'linear-gradient({self.angle}deg, {self.colour_1} 0%, {self.colour_2} 100%)'

    @property
    def view(self):
        return f'<div style="background: {self!s}; width: 100%;"></div>'
