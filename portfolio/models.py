from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify

class SiteSettings(models.Model):
    website_title = models.CharField(max_length=200, null=True, blank=True)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=300, blank=True)
    github_link = models.URLField(blank=True)
    linkedin_link = models.URLField(blank=True)
    twitter_link = models.URLField(blank=True)

    def __str__(self):
        return self.website_title

class HeroSection(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    subtitle = models.TextField(null=True, blank=True)
    badge_text = models.CharField(max_length=100, blank=True, null=True)
    hero_image = models.ImageField(upload_to='hero/', blank=True, null=True)
    cta_primary_text = models.CharField(max_length=50, default="Get Started")
    cta_primary_link = models.CharField(max_length=200, default="#contact")
    cta_secondary_text = models.CharField(max_length=50, default="Learn More")
    cta_secondary_link = models.CharField(max_length=200, default="#about")
    trust_indicator_text = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return "Hero Section"

class About(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='about/', blank=True, null=True)
    resume_file = models.FileField(upload_to='cv/', blank=True, null=True)
    resume_static = models.CharField(max_length=200, blank=True, null=True, help_text="Path to static resume file (e.g. 'portfolio/pdf/resume.pdf')")

    def __str__(self):
        return "About Section"

class Skill(models.Model):
    CATEGORY_CHOICES = (
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('tools', 'Tools'),
    )
    name = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='frontend')
    level = models.IntegerField(default=80)
    icon_name = models.CharField(max_length=50, blank=True, null=True) # e.g. 'python', 'react'

    def __str__(self):
        return self.name if self.name else "Unnamed Skill"

class Project(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    technologies_used = models.CharField(max_length=500, null=True, blank=True)
    github_link = models.URLField(blank=True, null=True)
    live_demo_link = models.URLField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    category = models.CharField(max_length=100, blank=True, null=True)
    seo_title = models.CharField(max_length=200, blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)
    keywords = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.title if self.title else "Unnamed Project"

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='projects/')

class Blog(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    content = RichTextField(null=True, blank=True)
    featured_image = models.ImageField(upload_to='blogs/', null=True, blank=True)
    tags = models.CharField(max_length=200, blank=True, null=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    meta_title = models.CharField(max_length=200, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.CharField(max_length=300, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title if self.title else "Unnamed Blog"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}" if self.name else "Anonymous Message"

class Testimonial(models.Model):
    client_name = models.CharField(max_length=100, null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    rating = models.IntegerField(default=5)
    profile_image = models.ImageField(upload_to='testimonials/', blank=True, null=True)

    def __str__(self):
        return self.client_name if self.client_name else "Unnamed Testimonial"

class Experience(models.Model):
    job_title = models.CharField(max_length=200, null=True, blank=True)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    duration = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.job_title} at {self.company_name}" if self.job_title and self.company_name else "Unnamed Experience"

