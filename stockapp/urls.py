from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from . import views

urlpatterns=[
			url(r'^$',views.home,name='stock'),
			url(r'^graph/',views.graph,name='graph'),
			url(r'^upload/',views.upload,name='upload'),
			url(r'^register/',views.register,name='register'),
			url(r'^login/',views.login1,name='login'),
			url(r'^logout/',views.logout_view,name='logout'),
			url(r'^list/',views.list,name='list'),
			url(r'^(?P<id>\d+)/',views.single_stock,name='single')

]
if settings.DEBUG:
    	    	urlpatterns += [
        url(r'^uploads/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),


] 