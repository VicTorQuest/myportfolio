from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse
from ckeditor.fields import RichTextField
# from PIL import Image

User = get_user_model()

# Create your models here.
class Service(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    icon = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    about = RichTextField()
    image = models.ImageField(upload_to='images')
    address = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    twitter = models.URLField()
    linkedin = models.URLField()
    github = models.URLField()
    discord = models.URLField()
    services = models.ManyToManyField(Service)

    class Meta:
        verbose_name_plural = "Portfolio"

    def __str__(self):
        return "{}'s Portfolio".format(self.user.first_name)

    def get_aboslute_url(self):
        return reverse('home')

class Tool(models.Model):
    name = models.CharField(max_length=50, unique=True)
    image = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ProjectCategory(models.Model):
    name = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name_plural = "Project Categories"

    def __str__(self):
        return self.name

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length = 20)
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    tools = models.ManyToManyField(Tool)
    live_url = models.URLField()
    github_repo = models.URLField()
    client = models.CharField(max_length=50, default="Personal")
    slug = models.SlugField(unique=True)
    date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            new_slug = slugify(self.title)
            self.slug = new_slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("project_detail", kwargs={"slug": self.slug})
    

class ProjectThumbnail(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='projectthumbnail')
    image = models.ImageField(upload_to="project_thumbnails")


    def __str__(self):
        return "{} thumbnail {}".format(self.project.title, self.id)

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     img = Image.open(self.image.path)

    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size, Image.Resampling.LANCZOS)
    #         img.save(self.image.path)

class Feedback(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    feedback = models.TextField()
    image = models.ImageField(upload_to="client image", null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}'s feedback".format(self.name)

class ProfessionalExperience(models.Model):
    role = models.CharField(max_length=100)
    duration = models.CharField(max_length=30, help_text='start year - end year')
    remote = models.BooleanField(default=True)
    experience = RichTextField()

    def __str__(self):
        return self.role

class Summary(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    info = RichTextField()

    class Meta:
        verbose_name_plural = "Summary"

    def __str__(self):
        return self.name

class Education(models.Model):
    degree = models.CharField(max_length=100)
    duration = models.CharField(max_length=30, help_text='start year - end year')
    institution = models.CharField(max_length=200)

    def __str__(self):
        return self.degree

