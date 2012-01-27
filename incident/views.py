from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from models import Incident, Cop, Force
from forms import IncidentForm, CopForm
from django.template import RequestContext, Context, loader
from django.core.exceptions import ObjectDoesNotExist

"""
Views for Incidents app

- needs to be broken up as app is modularised

"""


#list views

def recent(request):
	"""
	Returns list of all incidents most recent first using pagination
	helper.

	-should be generalisd and merged with other lists using subclass of
	django.models.detailview 
	"""
	recent_incidents = Incident.objects.order_by('-date','-time')
	incidents = paginate(request, recent_incidents)
	return render_to_response('incident_list.html', { 
								'incident_list' : incidents,
								'title'					: 'Recent Incidents',
								})


					
def cop_list(request, badge_search):
	"""
	Returns list of incidents involving a particular police officer in order of 
	date ( -date, -time ).

	Displays 'query header' giving information on the officer (name, badge, etc.)


	"""
	cop = Cop.objects.get(badge=badge_search.upper())
	events = {}
	for incident in cop.incident_set.all():
		if incident.event not in events:
			events[incident.event] = 1
		else:
			events[incident.event] += 1
  		
	cop_incidents = cop.incident_set.all().order_by('-time', '-date')
	cop_incidents = paginate(request, cop_incidents)
	graph = graph_from_template(events)
	return render_to_response('incident_list.html',{
							'title'					: 'cop search - %s' % cop,
							'incident_list' : cop_incidents,
							'graph' 				: graph,
							'query' 				: cop,
							'query_header' 	: True,
							 })
							 
def force_list(request, badge_code):
	force = Force.objects.get(badge=badge_code.upper())
	incidents = []
	events = {}
	for cop in force.cop_set.all():
		for i in cop.incident_set.all().order_by('-time', '-date'):
			if not i in incidents:
				if not i.event in events:
					events[i.event] = 1
				else: 
					events[i.event] += 1
				incidents.append(i)
	graph = graph_from_template(events)
	incidents =	paginate(request, incidents)
	return render_to_response('incident_list.html' ,{
							'title'					: 'force search - %s' % force,
							'incident_list' : incidents,
							'query' 				: force,
							'query_header' 	: True,
							'graph'				: graph,
							})
							 
#publish forms

def new(request):
	c = {}
	c.update(csrf(request))
	if request.method == 'POST':#if form has been submitted
		form = IncidentForm(request.POST, request.FILES) # a form bound to the POST data
		c.update({'form' : form})
		if form.is_valid(): #All validation rules pass
			i = form.save()
			if request.FILES:
				i.image = request.FILES['image']
				i.save()
			return HttpResponseRedirect('/incident/editcop_%s'% i.cop.all()[0]) # redirect after POST
	else:
		form = IncidentForm() # an unbound form
		c.update({'form': form})
	return render_to_response('new.html', c,
		 context_instance=RequestContext(request))

def update_cop(request, badge):
  c = {}
  c.update(csrf(request))
  c.update({'name': badge})
  cop = Cop.objects.get(badge=badge)
  if request.method == 'POST':
    form = CopForm(request.POST)
    if form.is_valid():
      if form['name'].value():      
        cop.name = form['name'].value()
        cop.save()
    return HttpResponseRedirect('/incident/recent')
  else:
    
    form = CopForm(instance=cop)
    c.update({'form': form})
  return render_to_response('editCop.html', c,
          context_instance=RequestContext(request))
  
  
# search views

def search(request):
	return HttpResponse('search')
	
def cop_search(request):
	return search(request, Cop)	

def force_search(request):
	response = search(request, Force)
	if response:
		return response

#helpers

def paginate(request, li):
	paginator = Paginator(li, 4)
	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page =  1
	try:
		incidents  = paginator.page(page)
	except (EmptyPage, InvalidPage):
		incidents = paginator.page(paginator.num_pages)
	return incidents
	
def search(request, model):
	errors = []
	mt1 = False
	if 'q' in request.GET:
		q = request.GET['q'].upper()
		if not q:
			errors.append('Enter a search term.')
		elif len(q) > 20:
			errors.append('Please enter at most 20 characters.')
		else:
				try:
					model.objects.get(badge=q.upper())   
					return HttpResponseRedirect('/incident/%s/%s'%(model.__name__.lower(), q))
				except model.DoesNotExist:
					tmp = model.objects.filter(badge__icontains=q)
					if tmp:
						if len(tmp) > 1:
							mt1 = True
						else:
							return HttpResponseRedirect('/incident/%s/%s'%(model.__name__.lower(), tmp[0].badge.lower()))
					else:
						tmp = model.objects.filter(name__icontains=q)
						if tmp:
							if len(tmp) > 1:
								mt1 = True

							return HttpResponseRedirect('/incident/%s/%s'%(model.__name__.lower(), tmp[0].badge.lower()))
						if mt1:
							return render_to_response('%s_list.html'%model.__name__.lower(), {
								'%ss_list'% model.__name__.lower()	: tmp,
								'query'															: q,
								})
					
						else:
							return HttpResponse('not found')

							
							
# Graaphs
def graph_from_template(data):
  t = loader.get_template('graph/graph.svg')  
  longest = max(data.values())*1.1
  data = [{'label': '%s: %s'%(x, y), 'width': (y/longest)*100, 'name': x} for x,y in data.items()]
  c = Context({'data': data })
  response = t.render(c)
  return response


