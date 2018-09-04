from django import forms 
		
class NewEntry(forms.Form):
	"""The form is to collect the users daly work"""
	movie = forms.IntegerField(max_value=24)
	self_study = forms.IntegerField(max_value=24)
	lectures = forms.IntegerField(max_value=24)
	exercise = forms.IntegerField(max_value=24)
	went_out = forms.IntegerField(max_value=24)
	sleep = forms.IntegerField(max_value=24)

class ChangeDp(forms.Form):
	"""The form is to handle dp uploads"""
	pic = forms.FileField()