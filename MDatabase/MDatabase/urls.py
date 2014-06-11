from django.conf.urls import patterns, include, url


from MDatabase import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',\
    # Examples:
    # url(r'^$', 'MDatabase.views.home', name='home'),
    url(r'^hello.html', views.hello, name='hello'),
	url(r'^network_data.html', views.network_data, name='network_data'),
	url(r'^controller_tag.html', views.controller_tag_render_func, name='controller_tag'),
    # Uncomment the admin/doc line below to enable admin documentation:
     
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),\
	 #Uncomment the next line to enable the admin:
	 url(r'^admin/', include(admin.site.urls)),
)
