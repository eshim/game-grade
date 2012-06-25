from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       
#    url(r'^$', 'gameandgrade.submissions.views.index',),
    # Current Task Stuff:
    url(r'^tasks/$', 'gameandgrade.submissions.views.allTasks',),
    url(r'^tasks/uploadFile/$', 'gameandgrade.submissions.views.uploadFile',),
    # New Task Stuff:
    url(r'^newTask/$', 'gameandgrade.submissions.views.createTask',),
    # Login / logout:
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    (r'^logout/$', 'gameandgrade.submissions.views.logout_page'),

    # Examples:
    # url(r'^$', 'gameandgrade.views.home', name='home'),
    # url(r'^gameandgrade/', include('gameandgrade.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
