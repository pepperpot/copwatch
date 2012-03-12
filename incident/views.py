from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from models import Incident, Cop, Force
from forms import IncidentForm, CopForm
from django.template import RequestContext, Context, loader
from django.core.exceptions import ObjectDoesNotExist
from django.utils import simplejson


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
	events, incidents = incidents_data('cop', cop)
	incidents = paginate(request, incidents)
	query_header = render_querybox('cop', cop, events)

	return render_to_response('incident_list.html',{
							'title'					: 'cop search - %s' % cop,
							'incident_list' : incidents,
							'query_header' 	: query_header,
							 })
							 
def force_list(request, badge_code):

  """ Returns list of incidents involving cops from a perticular force in order
  (-date, -time).
  
  Displays 'query_header' giving information on the police force (name, badge 
  reference. includes graph of incident types from incidents.views.graph
  """
  force = Force.objects.get(badge=badge_code.upper())
  events, incidents = incidents_data('force', force)
  query_header = render_querybox('force', force, events)
  incidents =	paginate(request, incidents)
  return render_to_response('incident_list.html' ,{
						  'title'					: 'force search - %s' % force,
						  'incident_list' : incidents,
						  'query_header'	: query_header,
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
    c.update({'form': form})
    if not form['name'].value() == cop.name:      
      cop.name = form['name'].value()
      cop.save()
      return HttpResponseRedirect('/incident/cop/%s'% badge)
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
def graph_from_template(data, width=180):
  if not data:
    return 'No recorded events..'
  t = loader.get_template('graph/graph.svg') 
  height = (len(data) + 2) * 10 
  longest = max(data.values()) # finds unit at end of x axis, giving buffer zone 
  data = [{'label': '%s: %s'%(x, y), 'width': (float(y)/longest)*width, 'name': x} for x,y in data.items()]
  grid_interval = float(width)/longest
  grid = [{'x': n, 'x_width': int((n*grid_interval)) + 100, 'width': (int(n*grid_interval))} for n in range(longest+1)]
  while len(grid) > 10:
    grid = [grid[n] for n in range(len(grid)) if n%2==0]
  c = Context({'data': data, 'grid': grid, 'height': height})
  response = t.render(c)
  return response

def render_querybox(model, instance, events, width = 8):
	if width == 8:
		graph_width = 180
	else:
		graph_width = 140
	graph = graph_from_template(events, graph_width)
	t = loader.get_template('partials/%s_box.html'% (model))
	c = Context({'%s' %(model): instance, 'graph': graph, 'size': width})
	query_box = t.render(c)
	return query_box
	
	
#copbox##

def copbox(request, badge):
  cop = Cop.objects.get(badge = badge.upper())
  events = incidents_data('cop', cop)[0]
  response = render_querybox('cop', cop, events, 4)
  return HttpResponse(response)

def incidents_data(model, instance):
	if model == 'cop':
		cop_set = [instance]
	else:
		cop_set = instance.cop_set.all()
	incidents = Incident.objects.filter(cop__in=cop_set).order_by('-time', '-date')
	events = {}
	for i in incidents:
		if not i.event in events:
			events[i.event] = 1
		else: 
			events[i.event] += 1
	return (events, incidents)

