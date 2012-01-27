from incident import models
import random
from datetime import datetime
import hatemaker
import os

def populate_forces():
  print 'Populating Force table.'
  t = open('incident/static/badge_numbers', 'r')
  lines = t.readlines()
  t.close()
  for l in lines:
    badge, name = l.split(':')
    f = models.Force(badge=badge.upper(), name=name.strip('\n'))
    f.save()
    print "Created Force instance '%s'." % f.name
  print '\nPopulated Force  table.\n\n'

def populate_cops():
  print 'Populating Cop table.' 
  forces = models.Force.objects.all()
  badges = [b.badge.upper() for b in forces]
  
  
  for n in range(100):
    force = random.choice(forces)
    n = random.randint(100,999)
    name = random.choice(['jon', 'july', 'jess', 'james', 'jim', 'jeff', 'julia', 'julie']).capitalize()
    c = models.Cop(badge="%s%s"%(force.badge, n), force=force, name = name)
    c.save()
    print "Created Cop instance '%s'." % c.badge
  print '\n Finished populating Cop table.\n\n'
  
def populate_incidents():
  print 'Populating Incident table...'  
  cops = models.Cop.objects.all()
  image_path = '/home/bob/copwatch/media/incident_images/'
  images = ["incident_images/%s" % img for img in os.listdir(image_path)]
  for n in range(100):
    image = random.choice(images)
    cop = random.choice(cops)
    event = random.choice(models.EVENT_TYPE_CHOICES)[1]
    date = datetime.now().date()
    time = datetime.now().time()
    location = random.choice(['darlington', 'scarborough', 'mersyside', 'hackney', 'hoxton', 'tottenham', 'manchester'])
    notes = hatemaker.incident_text()
    incident = models.Incident(event = event, date = date, time = time, loc = location, notes = notes, image = image)
    incident.save()
    incident.cop.add(cop)
    print "Created Incident instance '%s'." % incident.time
  print 'Finished populating Incident table.'
  
def main():
  populate_forces()
  populate_cops()
  populate_incidents()    

if __name__=='__main__':
  populate_forces()
