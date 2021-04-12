from django.urls import path, include
from . import views
from django.views.generic import TemplateView
from django.conf.urls import url
from django.urls import path, re_path

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('accounts/', include('allauth.urls')),
    url('auth/', views.MobileAuth), 
    url('authWeb/', views.WebAuth), 
    url('file/upload', views.FileUpload),

    #path('', TemplateView.as_view(template_name="templates/index.html")),

    # example: "www.digipackweb.com/drive/<gmail>"
    re_path(r'^drive/(?P<user>[\w.@+-]+)/$', views.InitDrive),

    # example: "www.digipackweb.com/gclass/<gmail>"
    re_path(r'^gclass/(?P<user>[\w.@+-]+)/$', views.InitGClass),

    # example: "www.digipackweb.com/sd/<gmail>/<fileid>"
    re_path(r'^sd/(?P<user>[\w.@+-]+)/(?P<fileid>[\w.@+-]+)$', views.DriveServerDownload),

    #path('goat.jpeg', views.DriveClientDownload),
    path('download/<str:filename>/', views.DriveClientDownload),

    # example: "www.digipackweb.com/pwa/<gmail>/<fileid>/<filename>"
    path('pwa/<str:user>/<str:fileid>/<str:filename>/', views.DrivePWADownload),
]

'''
    url(r'^sw.js', cache_control(max_age=2592000)(TemplateView.as_view(
    template_name="sw.js",
    content_type='application/javascript',
    )), name='sw.js'),
'''
