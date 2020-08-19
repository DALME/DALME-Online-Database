"""
This file is where all of the admin interface views are set up, available at
/admin
"""

from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import *

admin.site.register(Permission)
