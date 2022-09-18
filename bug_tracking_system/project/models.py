from django.db import models

# Create your models here.

class project(models.Model):
	name = models.CharField(max_length = 20)
	description = models.TextField(max_length = 300)
	date_added = models.DateField()
	bugs_count = models.IntegerField()

	def to_json(self):
		return {
		'name':self.name,
		'description':self.description,
		'date':str(self.date_added),
		"bugs_count":self.bugs_count
		}

