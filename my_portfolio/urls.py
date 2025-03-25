from django.urls import path
from .views import index, project_detail, submit_feedback, submit_email, get_blog_posts


urlpatterns = [
    path('', index, name='index'),
    path('#projects', index, name='my_works'),
    path('project-detail/<slug:slug>/', project_detail, name='project_detail'),
    path('submit-feedback/', submit_feedback, name='send_feedback'),
    path('submit-email/', submit_email, name='send_email'),
    path('get-blog-posts/', get_blog_posts, name='get_blog_posts')
]
