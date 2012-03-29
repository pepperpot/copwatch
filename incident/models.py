from django.db import models

class Force(models.Model):
	"""
	Force model (This class is static.)

	a list of police forces (at the moment only those within the MET)

	badge: one or two letter code
	name: name of police force

	-needs extra fields adding
	-eventually geodjango?
	"""

	badge = models.CharField(max_length=3, unique=True)
	name = models.CharField(max_length=60)

	def __unicode__(self):
		return self.name.capitalize()

class Cop(models.Model):
	"""
	Cop model

	Badge: one or two letters represent the department they work with, 3 numbers
	name: can be blank
	foce: foreignkey field to force model ( can be blank)
	"""
	badge = models.CharField(max_length=6, unique=True)
	name = models.CharField(max_length=20, blank=True)
	force = models.ForeignKey(Force, blank = True, null = True)

	def __unicode__(self):
		return self.badge

# current sample list of incident types
EVENT_TYPE_CHOICES = (
	('Stop and Search', 'Stop and Search'),
	('Arrest', 'Arrest'),
	('Beating', 'Beating'),
	('Kettle', 'Kettle'),
	('Verbal Abuse', 'Verbal Abuse'),
	('Other', 'Other'),
)

class Images(models.Model):
	"""
	Images model
	
	(to replace image attribute of Incident)
	
	Image: UnageField -  image file
	Caption: null=True, description of image
	Date: The date the image was added
	
	"""
	
	image = models.ImageField(upload_to = 'incident_images/')
	caption = models.CharField(max_length='200', null=True, blank=True)
	
	def __unicode__(self):
		return self.caption[:80]

class Incident(models.Model):

	"""
	Incident model

	Event: from EVENT_TYPE CHOICES
	Date: date in format YYYY-MM-DD
	Time: HH:MM:SS
	Loc/Location: Charfield ( wants updating/syncing to spatial database? )
	Notes: notes on incident. CharField.
	Cop: ManyToManyField with Cop model
	Image: image field. upload_to is rooted in MEDIA_ROOT

	"""
	event = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
	date = models.DateField()
	time = models.TimeField(blank=True, null=True)
	loc = models.CharField('location', max_length=100) 
	notes = models.CharField(max_length=2000)
	cop = models.ManyToManyField(Cop)
	image = models.ManyToManyField(Images, blank=True, null=True)

	def __unicode__(self):
		return self.notes[:10]
		

