from django.http import HttpResponse

#renders using modules from django.templates and responde with HttpResponse object
from django.shortcuts import render_to_response 
"""
Base level url views
"""

def home(request):
	return render_to_response('base.html')

def about(request):  
	return render_to_response('about.html')
	
def image(request, filename, filetype):
  """
  responds to url request to /incident_images/image.jpg with
  image from /media/incident_images/image.jpg
  
  -wants to be generalised
  """
  f = 'media/incident_images/%s.%s'% (filename.encode('utf-8'), filetype.encode('utf-8'))
  image = open(f)
  img = image.read()
  image.close()
  return HttpResponse(img, mimetype='image/%s' % filetype.encode('utf-8')) 
  
def thumb(request, thumb, filetype):

	f = 'media/incident_thumbs/%s.%s'%(thumb.encode(), filetype.encode())
	image = open(f)
	img = image.read()
	image.close()
	return HttpResponse(img, mimetype='image%s' % filetype.encode())
