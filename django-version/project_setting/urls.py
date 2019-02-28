"""horizontaladmintheme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from djdoc.views import AddEditDocument,ListDocument,ChangeVersion

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    ################### Add Document  & Edit Document URL ######################
    url(r'^add_doc/', login_required(AddEditDocument.as_view()), name='add_document'),
    url(r'^edit_doc/(?P<pk>[-\w]+)/$', login_required(AddEditDocument.as_view()), name='edit_document'),
    
    ########################## List Document URL ################################
    url(r'^list_doc/', login_required(ListDocument.as_view()), name='list_document'),
    
    ######################## Change Document params ContentType & InstanceId URL #######################
    url(r'^change_doc_vers/(?P<cntid>[-\w]+)/(?P<pk>[-\w]+)/$', login_required(ChangeVersion.as_view()), name='change_document'),
]
