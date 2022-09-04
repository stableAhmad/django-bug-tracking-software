from django.db import models


class team(models.Model):
    teamleader = models.CharField(null=False, blank=False, max_length=40)
    #teammembers = []
