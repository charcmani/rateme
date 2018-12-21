from django.db import models

# Create your models here.

class UserDetail(models.Model):
	"""Table to store the username and their respective
		score and other features"""
	username = models.CharField(max_length=50,primary_key=True)
	time_stamp = models.DateTimeField(auto_now=True)
	totMovie  = models.IntegerField(default=0)
	totStudy = models.IntegerField(default=0)
	totLectures = models.IntegerField(default=0)
	totExercise = models.IntegerField(default=0)
	totWent = models.IntegerField(default=0)
	totSleep = models.IntegerField(default=0)
	logs = models.IntegerField(default=0)
	pie = models.FileField(null=True)
	score = models.IntegerField(default=0)
	rating = models.IntegerField(default=0)
	dp = models.FileField(upload_to='.',default='default.jpeg')

class Entry(models.Model):
	"""Table to store entries of users"""
	id = models.AutoField(primary_key = True)
	username = models.ForeignKey(UserDetail,on_delete=models.CASCADE,db_column='username')
	time_stamp = models.DateTimeField(auto_now=True)
	movie  = models.IntegerField(default=0)
	self_study = models.IntegerField(default=0)
	lectures = models.IntegerField(default=0)
	exercise = models.IntegerField(default=0)
	went_out = models.IntegerField(default=0)
	sleep = models.IntegerField(default=0)

class RatingHistory(models.Model):
	"""
	Table to store rating of diff users
	"""
	username = models.ForeignKey(UserDetail,on_delete=models.CASCADE,db_column='username')
	rating = models.IntegerField(default=0)
	

 



		