from django.shortcuts import render
from django.views.generic.edit import CreateView,UpdateView,FormMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView,View
import datetime
from django.core.urlresolvers  import reverse
from django.contrib.contenttypes.models import ContentType
from django.http.response import HttpResponseRedirect
from djdoc.forms import DocumentForm
from djdoc.models import Document

from djversion.views import VersionViewMixin
# Create your views here.


# This class method overwrite CreateView CBV to manage 
# both Add form functions & Update form functions  
class AddEditDocument(VersionViewMixin):
    model=Document
    form_class =DocumentForm
    template_name = 'djdoc/generic_add.html'
    
    def form_valid(self, form, **kwargs):
        form.instance.created_by_id  = self.request.user.id
        form.instance.created_on   = datetime.datetime.now()
        form.instance.modified_by = self.request.user
        return super(AddEditDocument, self).form_valid(form)
    
    def get_context_data(self, **kwargs): 
       context = super(AddEditDocument, self).get_context_data(**kwargs)
       context['Title'] = 'Add Category'
       return context
    
    def get_success_url(self, *args, **kwargs):
        return reverse("list_document")
        
# List Document detail filter by current_version = True
class ListDocument(ListView):
     model = Document
     template_name = 'djdoc/generic_list.html'
     context_object_name = 'object'
     def get_queryset(self, **kwargs):
        return Document.objects.filter(current_version = True) 

# model.change_version_node function used to reverse old version     
# ChangeVersion function must pass contenttypeid & instanceid in url   
class ChangeVersion(View):
    def get(self, request, *args, **kwargs):
        cntid = self.kwargs['cntid']
        pk_id = self.kwargs['pk']
        cnt_type_obj = ContentType.objects.get(id = cntid)
        cnt_model = cnt_type_obj.model_class()
        cnt_model.change_version_node(cnt_model.objects.get(id=pk_id))
        return HttpResponseRedirect(reverse("list_document"))
        
   

