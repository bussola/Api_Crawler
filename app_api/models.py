from django.db import models

class Dados(models.Model):
	categoria = models.CharField(max_length=200, null=True)
	title = models.CharField(max_length=200)
	body = models.CharField(max_length=200)
	def __str__(self):
		return '%s %s' % (self.title, self.body)
