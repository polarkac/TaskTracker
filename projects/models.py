from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):

    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User)

    class Meta:
        unique_together = (('name', 'user'),)
