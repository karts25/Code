from django.conf.urls import patterns, url
from ladder import views

urlpatterns = patterns('',
                       url(r'^roster/$', views.roster, name='roster'),
                       url(r'^record/$', views.record, name='record'),
                       url(r'^recorded/$', views.recorded, name='recorded'),
                       url(r'^history/$', views.history, name='history'),
                       url(r'^singles/$',views.rankings_singles,name='rankings_singles'),
                       url(r'^doubles/$',views.rankings_doubles,name='rankings_doubles'),
)
