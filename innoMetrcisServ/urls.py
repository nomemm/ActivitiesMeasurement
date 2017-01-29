from django.conf.urls import include, url
from django.contrib import admin

from activities import views


urlpatterns = [
    url(r'^', include('activities.urls')),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include(
                           'rest_framework.urls', 
                           namespace='rest_framework'
		       )
       ),
    url(r'^measurements/', include('measurements.urls')),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
