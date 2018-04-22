from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns=[
    url(r'^$',views.home, name = 'home'),
    url(r'^form/$',views.model_form_upload,name = 'model_form_upload'),
    url(r'^emails-in-dir/$',views.emails_in_dir,name = 'emails_in_dir'),
    
    url(r'^show_email_payload/$',views.show_email_payload,name= 'show_email_payload'),
    url(r'^do_the_attachment_job/$',views.do_the_attachment_job,name= 'do_the_attachment_job'),
    url(r'^dirs_in_dir/$',views.dirs_in_dir,name= 'dirs_in_dir'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
