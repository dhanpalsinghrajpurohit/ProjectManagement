from django.forms import fields
from django.forms import ModelForm
from .models import Project, Task, ProjectPermission, Permission
from django import forms


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'featured_image',  'description',
                  'project_color_identity']

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name == "featured_image":
                field.widget.attrs.update({'class': 'form-control-file'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'placeholder':'Enter '+field.label})


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'project']
        widgets = {
            'project': forms.TextInput(attrs={'class':'form-control','readonly':True}),
            'project': forms.HiddenInput()
        }

    def __init__(self,*args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'placeholder': 'Enter ' + field.label})


class PermissionForm(ModelForm):
    class Meta:
        model = ProjectPermission
        fields = ['project', 'user', 'permission']
        widgets = {
            'permission': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super(PermissionForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == "permission":
                field.widget.attrs.update({'class': 'form-check form-check-inline m-2'})
            else:
                field.widget.attrs.update({'class':'form-control'})


