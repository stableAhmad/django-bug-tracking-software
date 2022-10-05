from django.db import models
from django.contrib.auth.models import User
from team.models import team
from project.models  import project

class report(models.Model):
    title = models.CharField(max_length=30)
    options = (
          ("S", "severe")
        , ("n", "noraml")
        , ("L", "mild")
    )
    severity = models.CharField(max_length=20, choices=options, default="high")
    description = models.TextField()
    attachment = models.FileField(upload_to='uploads/' , blank = True)
    states = (
          ("O", "open")
        , ("C", "closed")
        , ("R", "reopened")
    )
    users = User
    state = models.CharField(max_length=20, choices=states, default="open")
    date_added = models.DateField()
    reported_by = models.ForeignKey(User , related_name = "submitter", on_delete=models.DO_NOTHING, null=True, blank=True)
    assigned_to = models.ManyToManyField(User , related_name = "assigne")
    belongs_to = models.ForeignKey(project , on_delete = models.DO_NOTHING , null = True , blank = True)