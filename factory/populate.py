from incident import models
import random
from datetime import datetime
import hatemaker
import os
import Image

def populate_forces():
  print 'Populating Force table.'
  t = open('static_1/badge_numbers', 'r')
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
  forces = models.Force.objects.all()[1:11]
  badges = [b.badge.upper() for b in forces]
  
  
  for n in range(25):
    force = random.choice(forces)
    n = random.randint(100,999)
    name = random.choice(['jon', 'july', 'jess', 'james', 'jim', 'jeff', 'julia', 'julie']).capitalize()
    c = models.Cop(badge="%s%s"%(force.badge, n), force=force, name = name)
    c.save()
    print "Created Cop instance '%s'." % c.badge
  print '\n Finished populating Cop table.\n\n'

def populate_images():
  image_path = '/home/bob/copwatch/media/incident_images/'
  images = ["incident_images/%s" % img for img in os.listdir(image_path)]
  for image in images:
  	caption = 'a bunch of words, just to fill the attribute'
  	thumb = 'incident_thumbs/%s' % image.split('/')[-1]
  	tmb = Image.open('media/%s'%image)
  	tmb.thumbnail((120,120))
  	tmb.save('media/%s'%thumb)
  	i = models.Images( caption = caption, image = image, thumb = thumb)
  	
  	i.save()
  	print "Added image"
	
 
def populate_incidents():
  print 'Populating Incident table...'  
  cops = models.Cop.objects.all()
  images = models.Images.objects.all()
  for n in range(100):
    image_number = random.randint(0,3)
    cop_number = random.randint(1,4)
    image = []
    for n in range(image_number):
      i = random.choice(images)
      if not i in image:
        image.append(i)  	
    cop = []
    for n in range(cop_number):
      c = random.choice(cops)
      if not c in cop:
        cop.append(c)
    event = random.choice(models.EVENT_TYPE_CHOICES)[1]
    date = datetime.now().date()
    time = t = "%s:%s" % (datetime.now().hour, datetime.now().minute)
    location = random.choice(['darlington', 'scarborough', 'mersyside', 'hackney', 'hoxton', 'tottenham', 'manchester'])
    badge = cop[0].badge
    name = cop[-1].name
    notes = hatemaker.incident_text() % locals()
    incident = models.Incident(event = event, date = date, time = time, loc = location, notes = notes)
    incident.save()
    for c in cop:
      incident.cop.add(c)
    for i in image:
      incident.image.add(i)
    print "Created Incident instance '%s'." % incident.time
  print 'Finished populating Incident table.'
    
  
def clear(mods = [models.Incident,models.Cop,models.Force, models.Images]):
  if mods.__class__ != list:
    mods = [mods]
  for m in mods:
    for i in m.objects.all():
      i.delete()
    print 'cleared all instances of "%s"' % m

def main():
  clear()
  populate_images()
  populate_forces()
  populate_cops()
  populate_incidents()

if __name__=='__main__':
  populate_forces()
