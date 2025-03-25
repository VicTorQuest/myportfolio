from django.contrib import admin
from .models import Service, Portfolio, Tool, Project, ProjectCategory, Feedback, ProfessionalExperience, Summary, Education, ProjectThumbnail


# Register your models here.
class FeedbackAdmin(admin.ModelAdmin):
    search_fields = ['name', 'email']
    list_display = ['name', 'email', 'feedback', 'date']
    list_filter = ['date']

class Projectimages(admin.StackedInline):
    model = ProjectThumbnail

class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}
    inlines = [Projectimages]


admin.site.register(Service)
admin.site.register(Portfolio)
admin.site.register(Tool)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectCategory)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(ProfessionalExperience)
admin.site.register(Summary)
admin.site.register(Education)
admin.site.register(ProjectThumbnail)