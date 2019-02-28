from django.conf import settings
from django.db import models
from djversion.models import VersionModelMixin
# Create your models here.

# Create your models here.
STATUS = (
          (0,'Active'),
          (1,'InActive'),
          (2,'Trash')
          )

class Document(VersionModelMixin):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add = True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_Created_By')
    modified_on = models.DateTimeField(auto_now = True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_modified_by')
    status = models.IntegerField(choices=STATUS, default=0,verbose_name='Status')

    def __str__(self):
        return str(self.title)
