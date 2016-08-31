from __future__ import unicode_literals

from django.db import models
# Create your models here.

class users(models.Model):
	name=models.CharField(max_length=100)
	username=models.CharField(max_length=100)
	password=models.CharField(max_length=50)
	email=models.EmailField(max_length=100)

	def __str__(self):
		return self.name

class stock(models.Model):
	stock_name=models.CharField(max_length=100)
	stock_data=models.FileField(upload_to='uploads')
	def __str__(self):
		return self.stock_name

class index(models.Model):
	index_name=models.CharField(max_length=100)
	index_data=models.FileField(upload_to='uploads')
	def __str__(self):
		return self.index_name