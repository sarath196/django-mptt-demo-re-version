from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.contrib.contenttypes.models import ContentType

# Create your views here.
# Overwrite CreateView CBV
class VersionViewMixin(CreateView):
    # add instance data for update model
    def get_form_kwargs(self):
        kwargs = super(VersionViewMixin, self).get_form_kwargs()
        try:
            key = [karg for karg in self.kwargs.values()][0]
            object = self.model.objects.get(id = key)
            kwargs['instance'] = object
        except:
            pass
        return kwargs
    
    # add additional context data
    def get_context_data(self, **kwargs): 
       context = super(VersionViewMixin, self).get_context_data(**kwargs)
       cnttype_obj = ContentType.objects.get(model=self.model._meta.model_name)
       instance_kwarg = self.get_form_kwargs()
       instance = instance_kwarg['instance']
       if instance:
           context['related_tree_qs'] = self.model.get_version_node(instance) 
       context['model_content_type_id'] = cnttype_obj.id
       return context
       
    # add new version node
    def form_valid(self, form, **kwargs):
        form_instance = self.model.create_version_node(form)
        return super(VersionViewMixin, self).form_valid(form)
