from django.conf import settings
from django.db import models
from decimal import Decimal
from mptt.models import MPTTModel, TreeForeignKey

VERSION_STATUS = (
          (0,'Active'),
          (1,'InActive'),
          (2,'Trash')
          )

# Create your models here.
class VersionModelMixin(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='version_parent', verbose_name='Version Parent', db_index=True)
    version_no = models.DecimalField(max_digits=10,decimal_places=1,verbose_name='Version',default=0.1)
    current_version = models.BooleanField(default=True, verbose_name="Current Version")
    created_date = models.DateTimeField(auto_now_add = True)
    modified_date = models.DateTimeField(auto_now = True)
 
    class Meta:
        abstract = True
    ############## Create VersionNode & Update Version Node ###############
    def create_version_node(form, instance_id=None):
        # check if instance pass with instanceid, 
        # if True Create new version node and update old node version as false
        # if False simply create new version node and update as root parent
        if form.instance.id:
            parent_object = form._meta.model.objects.get(id = form.instance.id)
            form.instance.current_version  = True
            tree_obj = parent_object.get_family()
            ordered_obj = tree_obj.order_by('version_no')
            latest_obj = ordered_obj.last()
            form.instance.version_no =  round(Decimal(latest_obj.version_no) + Decimal(0.1),1)
            form.instance.parent_id = form.instance.id
            
            parent_object.current_version = False
            parent_object.save()
            
            form.instance.id = None
        else:
            form.instance.current_version  = True
            form.instance.version_no = 0.1
            form.instance.parent_id = None
        return form
    
    ######## Get Version Family #############
    def get_version_node(instance):
        return instance.get_family()
    
    ######## Change Version Node ###########
    def change_version_node(obj):
        obj_node = obj.get_family()
        for obj_qs in obj_node: 
            obj_qs.current_version = False
            obj_qs.save()
        obj.current_version = True
        obj.save()
        return obj