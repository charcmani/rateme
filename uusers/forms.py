from django import forms 
		
class NewEntry(forms.Form):
	"""The form is to collect the users daly work"""
	movie = forms.CharField()
	self_study = forms.CharField()
	lectures = forms.CharField()
	exercise = forms.CharField()
	went_out = forms.CharField()
	sleep = forms.CharField()

class ChangeDp(forms.Form):
	"""The form is to handle dp uploads"""
	pic = forms.FileField()