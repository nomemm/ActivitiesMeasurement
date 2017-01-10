from django.conf.urls import include, url
from django.contrib import admin



urlpatterns = [
    url(r'^', include('activities.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include(
                           'rest_framework.urls', 
                           namespace='rest_framework'
		       )
       ),
    url(r'^measurements/', include('measurements.urls')),
]
