from django.db import models
from django.contrib.auth.models import User
from team.models import team
from project.models import project
from user.views import user_to_json
from user.views import many_to_many_to_json


class report(models.Model):
    title = models.CharField(max_length=30)
    options = (
        ("Severe", "severe")
        , ("Normal", "normal")
        , ("Mild", "mild")
    )
    severity = models.CharField(max_length=20, choices=options, default="severe")
    description = models.TextField()
    attachment = models.FileField(upload_to='static/uploads/', blank=True)
    states = (
        ("Open", "open")
        , ("Closed", "closed")
        , ("Reopened", "reopened")
    )

    state = models.CharField(max_length=20, choices=states, default="open")
    date_added = models.DateField()
    reported_by = models.ForeignKey(User, related_name="submitter", on_delete=models.SET_NULL, null=True, blank=True)
    assigned_to = models.ManyToManyField(User, related_name="assign")
    belongs_to = models.ForeignKey(project, on_delete=models.SET_NULL, null=True, blank=True)

    def to_json(self):
        return_value = {
            'id':self.id,
            'title': self.title,
            'severity': self.severity,
            'description': self.description,
            'attachment': "temp",
            "state": self.state,
            "date_added": str(self.date_added),
            "reported_by": user_to_json(self.reported_by),
            "assigned_to": many_to_many_to_json(self.assigned_to),
            "belongs_to": self.belongs_to.to_json()
        }
        if self.attachment.name:
            return_value["attachment"]=self.attachment.url
        else:
            return_value["attachment"]=""
        return return_value    
        
