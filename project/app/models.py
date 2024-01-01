from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class TaskStatus(models.TextChoices):
    TODO = 'To Do', _('To Do')
    IN_PROGRESS = 'In Progress', _('In Progress')
    DONE = 'Done', _('Done')

class Team(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    members = models.ManyToManyField(User, related_name='teams')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.IntegerField()
    due_date = models.DateField()
    status = models.CharField(
        max_length=50,
        choices=TaskStatus.choices,
        default=TaskStatus.TODO,
    )
    team = models.ForeignKey(Team, related_name='tasks', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, related_name='created_tasks', on_delete=models.SET_NULL, null=True, blank=True)
    assignee = models.ForeignKey(User, related_name='assigned_tasks', on_delete=models.SET_NULL, null=True, blank=True)
    watchers = models.ManyToManyField(User, related_name='watched_tasks', blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.date}"

class Attachment(models.Model):
    task = models.ForeignKey(Task, related_name='attachments', on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    content = models.FileField(upload_to='attachments/')
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, related_name='attachments', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.file_name}"

class Label(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7)  # For hex color codes
    tasks = models.ManyToManyField(Task, related_name='labels')

    def __str__(self):
        return self.name
