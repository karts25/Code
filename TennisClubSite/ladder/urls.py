from django.conf.urls import patterns, url
from ladder import views

urlpatterns = patterns('',
                       url(r'^record/$', views.record, name='record'),
                       url(r'^recorded/$', views.recorded, name='recorded'),
                       url(r'^history/$', views.history, name='history'),
                       url(r'^rankings_singles/$',views.rankings_singles,name='rankings_singles'),
    #url(r'^(?P<pk>\d+)/results/$', views.results, name='results'),
)
