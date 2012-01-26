from django.http import HttpResponse
from django.shortcuts import render_to_response
from copwatch.incident.models import Incident

def home(request):
	return render_to_response('base.html')

def about(request):  
	return render_to_response('about.html')
	
def image(request, filename, filetype):
  f = 'media/incident_images/%s.%s'% (filename.encode('utf-8'), filetype.encode('utf-8'))
  image = open(f)
  img = image.read()
  image.close()
  return HttpResponse(img, mimetype='image/%s' % filetype.encode('utf-8')) 
