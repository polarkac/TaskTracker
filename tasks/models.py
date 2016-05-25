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

class Priority(models.Model):

    name = models.CharField(max_length=100, unique=True)

class Category(models.Model):

    name = models.CharField(max_length=150)

class Task(models.Model):

    name = models.CharField(max_length=200)
    description = models.TextField()
    project = models.ForeignKey(Project)
    priority = models.ForeignKey(Priority)
    category = models.ForeignKey(Category)
    created_date = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):

    content = models.TextField()
    task = models.ForeignKey(Task)
    created_date = models.DateTimeField(auto_now_add=True)

class TimeLog(models.Model):

    spend_time = models.PositiveIntegerField(default=0)
    comment = models.OneToOneField(Comment)

@receiver(post_save, sender=User)
def create_general_project(sender, instance, created, **kwargs):
    if created:
        Project.objects.create(
            name='General', description='Default project', user=instance,
            default=True
        )
