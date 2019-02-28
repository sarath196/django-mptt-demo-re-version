from django.views.generic.edit import CreateView
# abstract method to remove version fields
class VersionFormMixin(object):
    def __init__(self, *args, **kwargs):
        super(VersionFormMixin, self).__init__(*args, **kwargs) 
        self.fields.pop('parent')
        self.fields.pop('version_no')
        self.fields.pop('current_version')
        return 