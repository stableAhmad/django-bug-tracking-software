from django.db import models


class system(models.Model):
    system_name = models.CharField(max_length=30)
    system_mail = models.EmailField()
    system_password = models.CharField(max_length=30)
