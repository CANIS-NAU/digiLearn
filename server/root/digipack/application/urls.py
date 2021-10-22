from django.urls import path, include
from . import views
from . import webviews
from django.views.generic import TemplateView
from django.conf.urls import url
from django.urls import path, re_path

urlpatterns = [
    path('', webviews.index, name='index'),
    path('teacherconsole/', webviews.teacherconsole, name='teacherconsole'),
    path('login/', webviews.login, name='login'),
    path('teacherlogin/', webviews.teacherlogin, name ='teacherlogin'),
    path('accounts/', include('allauth.urls')),
    url('auth/', views.MobileAuth),
    url('authWeb/', webviews.WebAuth),
    url('teacherAuth/', webviews.teacherAuth),
    url('file/upload', views.FileUpload),
    url('search/', views.RetrieveQueries),
    url('submit/', views.FileSubmit),
    url('demosearch/', views.DemoQueries),
    url('createclass/', webviews.CreateClass),
    url('getclasses/', views.GetClasses),
    url('createassignment/', webviews.CreateAssignment),
    url('enroll/', webviews.EnrollStudents),

    path('searchdownload/<str:filename>', views.SearchClientDownload),

    url('archivesite/', views.ArchiveUrl),

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
