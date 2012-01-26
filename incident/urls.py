from django.conf.urls.defaults import patterns, include, url
import views

urlpatterns = patterns('',
	url(r'^recent/$', views.recent),
	url(r'^new/$', views.new),
	url(r'^search/$', views.search),
	url(r'cop/$', views.cop_search),
	url(r'^cop/(\w{2,6})/$', views.cop_list),
	url(r'^force/$', views.force_search),
	url(r'^force/(\D{1,3})/$', views.force_list),
	url(r'^editcop_(\w{2,6})/$', views.update_cop),

)
