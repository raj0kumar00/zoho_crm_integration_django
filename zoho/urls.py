
from django.urls import path, include
from django.conf.urls import include, url
from zoho import views
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('', views.home.as_view(), name = "home"),
	path('zohoadmin/', views.zohoadmin.as_view(), name = "zohoadmin" ),
	path('mytoken/', views.mytoken.as_view(), name= "mytoken"),
	url(r'^profile/$', login_required(login_url='/login')(views.profile.as_view()), name = "profile"),
	url(r'^register/$', views.register.as_view(), name = 'register'),
	url(r'^login/$', views.userlogin.as_view(), name='userlogin'),
	url(r'^logout/$', views.userlogout, name="userlogout"),
	url(r'^editprofile/$',login_required(login_url='/login')(views.editprofile.as_view()), name ='editprofile'),
	url(r'^errorpage/$',views.errorpage,name = "errorpage"),
	url(r'^test/$',views.test, name= "test")
]
