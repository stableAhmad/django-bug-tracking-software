from django.db import models

# Create your models here.

class project(models.Model):
	name = models.CharField(max_length = 20)
	description = models.TextField(max_length = 300)
	date_added = models.DateField()
	bugs_count = models.IntegerField()

