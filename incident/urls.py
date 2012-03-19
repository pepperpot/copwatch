from django.conf.urls.defaults import patterns, include, url
import views

urlpatterns = patterns('',
	url(r'^(\d{1,5})/', views.incident_detail),
	url(r'^recent/$', views.recent),
	url(r'^new/$', views.new),
	url(r'^search/$', views.search),
	url(r'cop/$', views.cop_search),
	url(r'^cop/(\w{2,6})/$', views.cop_list),
	url(r'^force/$', views.force_search),
	url(r'^force/(\D{1,3})/$', views.force_list),
	url(r'^editcop_(\w{2,6})/$', views.update_cop),
	url(r'^copform/([\w\s,]{2,20})/$', views.copform),
	url(r'^copbox(\w{2,6})/$', views.copbox),
	url(r'^copsave/([\w\s;]{5,25})$', views.copsave),

)
