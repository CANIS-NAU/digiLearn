from django.urls import path, include
from . import views
from django.views.generic import TemplateView
from django.conf.urls import url
from django.urls import path, re_path

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('accounts/', include('allauth.urls')),
    path('', TemplateView.as_view(template_name="templates/index.html")),

    # example: "www.digipackweb.com/user/<gmail>"
    re_path(r'^user/(?P<user>[\w.@+-]+)/$', views.InitDrive),

    # example: "www.digipackweb.com/sd/<gmail>/<fileid>"
    re_path(r'^sd/(?P<user>[\w.@+-]+)/(?P<fileid>[\w.@+-]+)$', views.DriveServerDownload),

    # example: "www.digipackweb.com/cd/<gmail>/<filename>"
    #re_path(r'^cd/(?P<userid>[\w.@+-]+)/(?P<filename>[\w.@+-]+)$', views.DriveClientDownload),
    #path('goat.jpeg', views.DriveClientDownload),
    path('download/<str:filename>/', views.DriveClientDownload),

    url('auth/', views.MobileAuth), #possibly remove the trailing "/"
]