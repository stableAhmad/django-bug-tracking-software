from django.db import models
from django.contrib.auth.models import User
from team.models import team


class report(models.Model):
    title = models.CharField(max_length=30)
    options = (
          ("S", "severe")
        , ("M", "moderate")
        , ("L", "mild")
    )
    severity = models.CharField(max_length=20, choices=options, default="high")
    description = models.TextField()
    attachment = models.FileField(upload_to='uploads/')
    states = (
          ("O", "open")
        , ("C", "closed")
        , ("R", "reopened")
    )
    users = User
    state = models.CharField(max_length=20, choices=states, default="open")
    date_added = models.DateField()
    reported_by = models.OneToOneField(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    assigned_to = models.OneToOneField(team, on_delete=models.DO_NOTHING, default=1, null=True, blank=True)
