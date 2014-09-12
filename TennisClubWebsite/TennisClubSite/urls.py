from django.conf.urls import patterns, include, url
from django.contrib import admin
import views

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                           # url(r'^$', 'TennisClubSite.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^ladder/', include('ladder.urls',namespace="ladder")),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^index/$',views.index,name='index'),
                       url(r'^about/$',views.about,name='about'),
                       url(r'^news/$',views.news,name='news'),
                       #url(r'^roster/$',views.ladder,name='ladder'),
                       url(r'^media/$',views.media,name='media'),
                       url(r'^faq/$',views.faq,name='faq'),
                       url(r'^contact/$',views.contact,name='contact'),
                       )
