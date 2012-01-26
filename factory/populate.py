from incident import models
import random

def populate_forces():
  t = open('incident/static/badge_numbers', 'r')
  lines = t.readlines()
  t.close()
  for l in lines:
    badge, name = l.split(':')
    f = models.Force(badge=badge, name=name.strip('\n'))
    f.save()

def populate_cops():
  forces = models.Forces.objects.all()
  badges = [b.badge for b in forces]
  for n in range(100):
    force = random.choice(forces)
    n = random.randint(100,999)
    name = random.choice(['jon', 'july', 'jess', 'james', 'jim', 'jeff', 'julia', 'julie']).capitalize()
    c = models.Cop(badge="%s%s"%(force.badge, n), force=force.id, name = name)
    c.save()
    

if __name__=='__main__':
  populate_forces()
