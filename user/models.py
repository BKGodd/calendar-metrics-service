from django.db import models
from uuid import uuid4


class User(models.Model):
    # Use our own UUID in order to create the watch channel for Google Calendar
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField('name', max_length=240)
    email = models.EmailField(unique=True)
    created = models.DateField(auto_now_add=True)
    # Other stats from the calendar could go here, if desired
