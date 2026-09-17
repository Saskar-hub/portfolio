from django import forms
from .models import (
    SiteSettings, HeroSection, About, Skill, Project,
    Blog, ContactMessage, Testimonial, Experience
)
from ckeditor.widgets import CKEditorWidget

class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = '__all__'

class HeroSectionForm(forms.ModelForm):
    class Meta:
        model = HeroSection
        fields = '__all__'

class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = '__all__'

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'

class ProjectForm(forms.ModelForm):
    uploaded_images = forms.FileField(
        required=False,
        label="Upload Project Images",
        widget=forms.ClearableFileInput(attrs={'class': 'upload-project-images'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['uploaded_images'].widget.attrs['multiple'] = 'multiple'

    class Meta:
        model = Project
        fields = '__all__'

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message', 'is_read']

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = '__all__'

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = '__all__'
