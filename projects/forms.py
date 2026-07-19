from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):
    """Collect the user-editable details for a new project."""

    technology_stack = forms.CharField(
        max_length=255,
        required=False,
        label='Technology stack',
        help_text='For example: Django, PostgreSQL, and React.',
    )

    class Meta:
        model = Project
        fields = ('name', 'description', 'technology_stack', 'complexity')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g. Customer support portal'}),
            'description': forms.Textarea(
                attrs={
                    'rows': 5,
                    'placeholder': 'Describe the problem, users, and intended outcome.',
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['technology_stack'].initial = self.instance.technology

    def save(self, commit=True):
        project = super().save(commit=False)
        project.technology = self.cleaned_data['technology_stack']
        if commit:
            project.save()
            self.save_m2m()
        return project
