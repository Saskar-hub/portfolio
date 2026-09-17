import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')
django.setup()

from portfolio.models import SiteSettings, HeroSection, About, Skill, Project, Experience, Testimonial

def seed():
    # 1. Site Settings
    if not SiteSettings.objects.exists():
        SiteSettings.objects.create(
            website_title="My Portfolio",
            meta_title="Professional Developer Portfolio",
            meta_description="Welcome to my portfolio website.",
            meta_keywords="developer, portfolio, django, python",
            github_link="https://github.com/",
            linkedin_link="https://linkedin.com/",
            twitter_link="https://twitter.com/",
        )
        print("SiteSettings created.")

    # 2. Hero Section
    if not HeroSection.objects.exists():
        HeroSection.objects.create(
            title="Scale Your Future",
            subtitle="Crafting high-performance digital experiences with cutting-edge technology. We turn your vision into scalable reality.",
            badge_text="Available for Hire",
            cta_primary_text="Get Started",
            cta_primary_link="#contact",
            cta_secondary_text="Learn More",
            cta_secondary_link="#about",
            trust_indicator_text="Trusted by 50+ clients worldwide"
        )
        print("HeroSection created.")

    # 3. About Section
    if not About.objects.exists():
        About.objects.create(
            title="About Me",
            description="I am a professional developer with passion for building modern web applications.",
        )
        print("About created.")

    # 4. Skills
    if not Skill.objects.exists():
        skills = [
            ('Python', 'backend', 95, 'python'),
            ('Django', 'backend', 90, 'django'),
            ('React', 'frontend', 85, 'react'),
            ('HTML5/CSS3', 'frontend', 95, 'html5'),
            ('Docker', 'tools', 80, 'docker'),
            ('Git', 'tools', 90, 'git'),
        ]
        for name, category, level, icon in skills:
            Skill.objects.create(name=name, category=category, level=level, icon_name=icon)
        print("Skills created.")

    # 5. Projects
    if not Project.objects.exists():
        Project.objects.create(
            title="E-commerce Platform",
            description="A scalable e-commerce platform built with Django and React.",
            technologies_used="Django, React, PostgreSQL",
            is_featured=True,
            category="Web Development"
        )
        print("Project created.")

    # 6. Experience
    if not Experience.objects.exists():
        Experience.objects.create(
            job_title="Senior Developer",
            company_name="Tech Corp",
            duration="Jan 2021 - Present",
            description="Leading the development of modern web apps."
        )
        print("Experience created.")

    # 7. Testimonials
    if not Testimonial.objects.exists():
        Testimonial.objects.create(
            client_name="Jane Smith",
            feedback="Excellent work! Highly recommended.",
            rating=5
        )
        print("Testimonial created.")

if __name__ == "__main__":
    seed()
