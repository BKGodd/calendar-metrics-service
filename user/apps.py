from django.apps import AppConfig
import json
from django.utils import timezone
import uuid

class UserConfig(AppConfig):

    def ready(self):
        """First time code to run when startup."""
        return