from django import forms
from incident.models import *
import re
from django.core.exceptions import ObjectDoesNotExist
import datetime

class IncidentForm(forms.ModelForm):

	class Meta:
		model = Incident
		exclude = ('cop', 'image')
		
	notes = forms.CharField(widget=forms.Textarea(attrs={'cols': 27, 'rows': 6}))
	attrs = {'enctype':"multipart/form-data",}
	date = forms.CharField(max_length=10, initial=datetime.date.today().strftime('%d/%m/%Y'))
		

			
			
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
		exclude = ('date')
