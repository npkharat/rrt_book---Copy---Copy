from django.db import models
from django.contrib.auth.models import User

class Component(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Issue(models.Model):
    component = models.ForeignKey(Component, related_name='issues', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    troubleshooting = models.TextField(max_length=255)
    action_plan = models.TextField(max_length=255)
    error_message = models.TextField(max_length=255)
    spare_part = models.TextField(max_length=255)
    advisory = models.TextField(max_length=255)
    log_below_gen8 = models.TextField(max_length=255)
    log_above_gen8 = models.TextField(max_length=255)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Issue for {self.component.name} by {self.user.username}"
