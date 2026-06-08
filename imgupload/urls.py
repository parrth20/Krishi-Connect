
from django.contrib import admin

from django.urls.conf import include
from . import views
from django.urls import include, path

urlpatterns = [
    path('imageprocess',views.imageprocess,name='imageprocess'),
    path('imgupload', views.imgupload, name='upload'),
    path('samplediagnosis/<slug:slug>', views.sample_diagnosis, name='sample_diagnosis'),
    path('report', views.report, name='report'),

    

    
]
