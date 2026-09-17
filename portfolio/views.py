from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django import forms
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import (
    SiteSettings, HeroSection, About, Skill, Project, 
    Blog, ContactMessage, Testimonial, Experience, ProjectImage
)
from .serializers import (
    SiteSettingsSerializer, HeroSectionSerializer, AboutSerializer, 
    SkillSerializer, ProjectSerializer, BlogSerializer, 
    ContactMessageSerializer, TestimonialSerializer, ExperienceSerializer
)
from django import forms as django_forms
from .forms import (
    SiteSettingsForm, HeroSectionForm, AboutForm, SkillForm, 
    ProjectForm, BlogForm, ContactMessageForm, TestimonialForm, ExperienceForm
)

# --- API ViewSets ---

class SiteSettingsViewSet(viewsets.ModelViewSet):
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return SiteSettings.objects.all()[:1]

class HeroSectionViewSet(viewsets.ModelViewSet):
    queryset = HeroSection.objects.all()
    serializer_class = HeroSectionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class AboutViewSet(viewsets.ModelViewSet):
    queryset = About.objects.all()
    serializer_class = AboutSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_projects = self.queryset.filter(is_featured=True)
        serializer = self.get_serializer(featured_projects, many=True)
        return Response(serializer.data)

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    @action(detail=False, methods=['get'])
    def published(self, request):
        published_blogs = self.queryset.filter(is_published=True)
        serializer = self.get_serializer(published_blogs, many=True)
        return Response(serializer.data)

class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# --- Public Template View ---

def index(request):
    settings = SiteSettings.objects.first()
    hero = HeroSection.objects.first()
    about = About.objects.first()
    projects = Project.objects.all()
    skills = Skill.objects.all()
    experiences = Experience.objects.all()
    testimonials = Testimonial.objects.all()
    blogs = Blog.objects.filter(is_published=True)[:3]

    context = {
        'site_settings': settings,
        'hero': hero,
        'about': about,
        'projects': projects,
        'skills': skills,
        'experiences': experiences,
        'testimonials': testimonials,
        'blogs': blogs,
    }
    return render(request, 'portfolio/index.html', context)

# --- Custom Admin Views ---

def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

@login_required
@superuser_required
def admin_dashboard(request):
    stats = {
        'projects': Project.objects.count(),
        'blogs': Blog.objects.count(),
        'messages': ContactMessage.objects.count(),
        'skills': Skill.objects.count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
    }
    recent_messages = ContactMessage.objects.all().order_by('-timestamp')[:5]
    return render(request, 'portfolio/admin/admin_dashboard.html', {
        'stats': stats,
        'recent_messages': recent_messages
    })

@login_required
@superuser_required
def admin_hero(request):
    instance = HeroSection.objects.first()
    if request.method == 'POST':
        form = HeroSectionForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hero section updated successfully!')
            return redirect('admin_hero')
    else:
        form = HeroSectionForm(instance=instance)
    return render(request, 'portfolio/admin/admin_form.html', {
        'form': form,
        'title': 'Hero Section'
    })

@login_required
@superuser_required
def admin_about(request):
    instance = About.objects.first()
    if request.method == 'POST':
        form = AboutForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'About section updated successfully!')
            return redirect('admin_about')
    else:
        form = AboutForm(instance=instance)
    return render(request, 'portfolio/admin/admin_form.html', {
        'form': form,
        'title': 'About Section'
    })

@login_required
@superuser_required
def admin_settings(request):
    instance = SiteSettings.objects.first()
    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Site settings updated successfully!')
            return redirect('admin_settings')
    else:
        form = SiteSettingsForm(instance=instance)
    return render(request, 'portfolio/admin/admin_form.html', {
        'form': form,
        'title': 'Global Settings'
    })

@login_required
@superuser_required
def admin_list(request, model_name):
    model_map = {
        'projects': (Project, 'Projects'),
        'blogs': (Blog, 'Blogs'),
        'skills': (Skill, 'Skills'),
        'testimonials': (Testimonial, 'Testimonials'),
        'experience': (Experience, 'Experience'),
        'messages': (ContactMessage, 'Contact Messages'),
    }
    model_info = model_map.get(model_name)
    if not model_info:
        return redirect('admin_dashboard')
    
    model, title = model_info
    items = model.objects.all().order_by('-id')
    return render(request, 'portfolio/admin/admin_list.html', {
        'items': items,
        'title': title,
        'model_name': model_name
    })

@login_required
@superuser_required
def admin_add_item(request, model_name):
    form_map = {
        'projects': (ProjectForm, 'Project'),
        'blogs': (BlogForm, 'Blog'),
        'skills': (SkillForm, 'Skill'),
        'testimonials': (TestimonialForm, 'Testimonial'),
        'experience': (ExperienceForm, 'Experience'),
    }
    form_info = form_map.get(model_name)
    if not form_info:
        return redirect('admin_dashboard')
        
    form_class, title = form_info
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            if model_name == 'projects':
                images = request.FILES.getlist('uploaded_images')
                for img in images:
                    ProjectImage.objects.create(project=obj, image=img)
            messages.success(request, f'{title} added successfully!')
            return redirect('admin_list', model_name=model_name)
    else:
        form = form_class()
    return render(request, 'portfolio/admin/admin_form.html', {
        'form': form,
        'title': f'Add {title}',
        'model_name': model_name
    })

@login_required
@superuser_required
def admin_edit_item(request, model_name, pk):
    model_map = {
        'projects': (Project, ProjectForm, 'Project'),
        'blogs': (Blog, BlogForm, 'Blog'),
        'skills': (Skill, SkillForm, 'Skill'),
        'testimonials': (Testimonial, TestimonialForm, 'Testimonial'),
        'experience': (Experience, ExperienceForm, 'Experience'),
        'messages': (ContactMessage, ContactMessageForm, 'Message'),
    }
    model_info = model_map.get(model_name)
    if not model_info:
        return redirect('admin_dashboard')
        
    model, form_class, title = model_info
    instance = get_object_or_404(model, pk=pk)
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            obj = form.save()
            if model_name == 'projects':
                images = request.FILES.getlist('uploaded_images')
                for img in images:
                    ProjectImage.objects.create(project=obj, image=img)
            messages.success(request, f'{title} updated successfully!')
            return redirect('admin_list', model_name=model_name)
    else:
        form = form_class(instance=instance)
    return render(request, 'portfolio/admin/admin_form.html', {
        'form': form,
        'title': f'Edit {title}',
        'model_name': model_name,
        'object': instance
    })

@login_required
@superuser_required
def admin_delete_item(request, model_name, pk):
    model_map = {
        'projects': Project,
        'blogs': Blog,
        'skills': Skill,
        'testimonials': Testimonial,
        'experience': Experience,
        'messages': ContactMessage,
    }
    model = model_map.get(model_name)
    if model:
        instance = get_object_or_404(model, pk=pk)
        instance.delete()
        messages.success(request, 'Item deleted successfully!')
    return redirect('admin_list', model_name=model_name)
