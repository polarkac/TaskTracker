from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum

class Project(models.Model):

    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User)
    default = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('name', 'user'),)
        ordering = ['-default', '-created_date']

class Priority(models.Model):

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Category(models.Model):

    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class TaskState(models.Model):

    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Task(models.Model):

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    project = models.ForeignKey(Project)
    priority = models.ForeignKey(Priority)
    category = models.ForeignKey(Category)
    created_date = models.DateTimeField(auto_now_add=True)
    state = models.ForeignKey(TaskState)
    paid = models.BooleanField(default=False)
    per_hour = models.PositiveSmallIntegerField(default=150)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.total_task_time = 0

    def get_payment(self):
        total_task_time = self.get_task_time()

        return (total_task_time / 60) * self.per_hour

    def get_task_time(self):
        if not self.total_task_time:
            time_logs = (
                TimeLog.objects.filter(comment__task=self)
                .aggregate(Sum('spend_time'))
            )

            self.total_task_time = time_logs['spend_time__sum']
            if not self.total_task_time:
                self.total_task_time = 0

        return self.total_task_time

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_date']

class Comment(models.Model):

    content = models.TextField()
    task = models.ForeignKey(Task)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s: %s'.format(self.task, self.created_date)

    class Meta:
        ordering = ['created_date']

class TimeLog(models.Model):

    spend_time = models.PositiveIntegerField(default=0)
    comment = models.OneToOneField(Comment)

    def __str__(self):
        return '%s: %s minutes'.format(self.comment.task, self.spend_time)

@receiver(post_save, sender=User)
def create_general_project(sender, instance, created, **kwargs):
    if created:
        Project.objects.create(
            name='General', description='Default project', user=instance,
            default=True
        )
