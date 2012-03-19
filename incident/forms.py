from django import forms
from incident.models import *
import re
from django.core.exceptions import ObjectDoesNotExist
import datetime

class IncidentForm(forms.ModelForm):

	class Meta:
		model = Incident
		
	notes = forms.CharField(widget=forms.Textarea(attrs={'cols': 27, 'rows': 6}))
	cop = forms.CharField(widget=forms.Textarea(attrs={'cols':15, 'rows': 1,'onMouseOut': "returnCopForm(xmlhttp)"}))
	attrs = {'enctype':"multipart/form-data",}
	date = forms.CharField(max_length=10)
		
	def clean_cop(self):
		cop = self.cleaned_data['cop'].split(',')
		cleaned_cop = []
		for c in cop:
			c = c.strip().upper()
			force = re.search(r'^([\D]{1,3})', c).groups()[0].upper()
			try:
				force = Force.objects.get(badge=force)
			except Force.DoesNotExist: 
				force = False
			if force:
				Cop.objects.get_or_create(badge=c, force=force)
			else:
				Cop.objects.get_or_create(badge=c)
			cleaned_cop.append(Cop.objects.get(badge=c))
		return cleaned_cop

	def clean_date(self):
		pattern = r'([\d]{1,2})[-|/]([\d]{1,2})[-|/]([\d]{4})'
		date = self.cleaned_data['date'].encode()
		try:
			d,m,y = re.search(pattern, date).groups()
			date = datetime.date(int(y),int(m),int(d))
		except AttributeError:
			date = False
		return date
			
			
		
class CopForm(forms.ModelForm):
	class Meta:
		model = Cop
		
class ImagesForm(forms.ModelForm):
	class Meta:
		model = Images
