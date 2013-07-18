from django.conf.urls import patterns, include, url
from django.contrib   import admin

admin.autodiscover()

urlpatterns = patterns('gameandgrade.submissions.views',
    # Task View
    url(r'^tasks/$', 'viewTasks',),
    # Upload View
    url(r'^tasks/uploadFile/$', 'uploadFile',),
    # UploadPaste View
    url(r'^uploadCode/$', 'uploadCode'),
    # Logout View
    url(r'^logout/$', 'logout_page'),
    # New Submissions View
    url(r'^subs/$', 'newSub'),
    # Submissions View
    url(r'^tasks/(?P<taskID>\d+)/(?P<subID>\d+)/$', 'viewSub'),
)

urlpatterns += patterns('',                     
    # Admin Site
    url(r'^admin/', include(admin.site.urls)),
    # Login Page
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    
    # Examples:
    # url(r'^$', 'gameandgrade.views.home', name='home'),
    # url(r'^gameandgrade/', include('gameandgrade.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)