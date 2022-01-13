from django.forms import fields
from django.forms import ModelForm
from .models import Project, Task
from django import forms


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'featured_image',  'description',
                  'project_color_identity']

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name=="featured_image":
                field.widget.attrs.update({'class': 'form-control-file'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'placeholder':'Enter '+field.label})


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description','project', 'assigned_to']


    def __init__(self,*args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'placeholder': 'Enter ' + field.label})
