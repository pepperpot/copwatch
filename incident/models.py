from django.db import models

class Force(models.Model):
	badge = models.CharField(max_length=3)
	name = models.CharField(max_length=60)

	def __unicode__(self):
		return self.name.capitalize()

class Cop(models.Model):
	badge = models.CharField(max_length=6)
	name = models.CharField(max_length=20, blank=True)
	force = models.ForeignKey(Force, blank = True, null = True)

	def __unicode__(self):
		return self.badge


EVENT_TYPE_CHOICES = (
	('Stop and Search', 'Stop and Search'),
	('Arrest', 'Arrest'),
	('Beating', 'Beating'),
	('Kettle', 'Kettle'),
	('Verbal Abuse', 'Verbal Abuse'),
	('Other', 'Other'),
)

class Incident(models.Model):
	event = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
	date = models.DateField()
	time = models.TimeField(blank=True, null=True)
	loc = models.CharField('location', max_length=100) 
	notes = models.CharField(max_length=2000)
	cop = models.ManyToManyField(Cop)
	image = models.ImageField(upload_to = 'incident_images/', blank=True, null=True)

	def __unicode__(self):
		return self.notes[:10]
		
	
