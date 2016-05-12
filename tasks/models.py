from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Project(models.Model):

    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User)
    default = models.BooleanField(default=False)

    class Meta:
        unique_together = (('name', 'user'),)

@receiver(post_save, sender=User)
def create_general_project(sender, instance, created, **kwargs):
    if created:
        Project.objects.create(
            name='General', description='Default project', user=instance,
            default=True
        )
