from django.db import models


class team(models.Model):
    teamleadermail = models.EmailField(null=True , default = "non_assigned")
    
   