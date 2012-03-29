from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from models import Incident, Cop, Force, Images
from forms import IncidentForm, CopForm, ImagesForm
from django.template import RequestContext, Context, loader
from django.core.exceptions import ObjectDoesNotExist
from django.utils import simplejson
from django.forms.models import modelformset_factory
import re

def new(request):
	cop_form_set = modelformset_factory(Cop, extra=2,)
	image_form_set = modelformset_factory(Images, extra=4)
	c = {}
	c.update(csrf(request))
	if request.method == 'POST':#if form has been submitted
		incidentForm = IncidentForm(request.POST, prefix='incident') # a form bound to the POST data
		copFormSet = cop_form_set(request.POST, prefix='cop')
		imageFormSet = image_form_set(request.POST, request.FILES, prefix='images')
		if incidentForm.is_valid() and copFormSet.is_valid() and imageFormSet.is_valid():
			cops = copFormSet.save()
			images = imageFormSet.save()
			incident = incidentForm.save()
			for cop in request.POST['incident-cop_string'].split(','):
				incident.cop.add(Cop.objects.get(badge=cop.strip()))
			for image in images:
				incident.image.add(image)
				image.date = incident.date
				image.save()
			incident.save()	
			return HttpResponseRedirect('/incident/%s'%incident.id)	
	else:
		incidentForm = IncidentForm(prefix='incident') # an unbound form
		copFormSet = cop_form_set(queryset = Cop.objects.none(),prefix='cop')
		imageFormSet = image_form_set(queryset = Images.objects.none(), prefix='images')
	c.update({'incident_form': incidentForm, 'cop_form': copFormSet, 'image_form': imageFormSet})
	return render_to_response('test/new.html', c,
		 context_instance=RequestContext(request))
		 
def copform(request,cop_string):
	cop_list = [cop.strip().upper() for cop in cop_string.encode().split(',')]
	try:
		cop_exists_list = Cop.objects.filter(badge__in=cop_list)
	except Cop.DoesNotExist:
		cop_exists_list = []
	cop_new_list = [cop for cop in cop_list if not cop in [c.badge for c in cop_exists_list]]
	cop_new_tuples = []
	for cop in cop_new_list:
		try:
			force = Force.objects.get(badge = re.search(r'^([\D]{1,3})', cop).groups()[0].upper())
		except Force.DoesNotExist:
			force = Force.objects.all()[0]
		cop_new_tuples.append((cop, force))
		
	cop_form_set = modelformset_factory(Cop, extra=len(cop_new_list))
	copFormSet = cop_form_set(queryset=Cop.objects.none(), prefix='cop', initial=[{'badge':badge, 'force':force}  for badge, force in cop_new_tuples])
	return render_to_response('copformset.html', {'copformset': copFormSet, 'cop_exists': cop_exists_list})
	
