from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
app_name = 'upload_example'

#urlpatterns = [
#    url(r'^$', views.home, name='home'),
#    url(r'^simple/$', views.simple_upload, name='simple_upload'),
#    url(r'^form/$', views.model_form_upload, name='model_form_upload'),
#    url(r'^admin/', admin.site.urls),
#]

urlpatterns = [
    path('', views.home, name='home'),
    path('simple/', views.simple_upload, name='simple_upload'),
    path('form/', views.model_form_upload, name='model_form_upload'),
]
