import json
import os
import requests
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render, get_object_or_404
from .models import Portfolio, Tool, Feedback, ProfessionalExperience, Education, Summary, Service, Project, ProjectCategory


User = get_user_model()
my_user = User.objects.filter(username='Victor').first()

# Create your views here.
def index(request):
    my_portfolio = Portfolio.objects.get(user=my_user)
    email = my_user.email
    tools = Tool.objects.all()
    feedbacks = Feedback.objects.all()
    all_experience = ProfessionalExperience.objects.all()
    summary = Summary.objects.get(user=my_user)
    education = Education.objects.all()
    services = Service.objects.all()
    projects = Project.objects.all()
    project_categories = ProjectCategory.objects.all()
    return render(request, 'my_portfolio/index.html', {
        'email': email,
        'tools': tools,
        'feedbacks': feedbacks,
        'all_experience': all_experience,
        'summary': summary,
        'education': education,
        'services': services,
        'my_portfolio': my_portfolio,
        'projects': projects,
        'project_categories': project_categories
    })


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'my_portfolio/project-details.html', {
        'project': project
    })

def submit_feedback(request):
    if request.method == 'POST':
        try:
            name =request.POST.get('name')
            email = request.POST.get('email')
            feedback = request.POST.get('message')
            image = request.FILES.get('image')
            Feedback.objects.create(name=name, email=email, feedback=feedback, image=image)
            message = 'Your feedback was sent, thank you'
            # send_mail('New feedback message from {}'.format(name), feedback, email, [my_user.email], fail_silently=True)
            return JsonResponse({'message': message, 'success': True})
        except:
            message = "Feedback wasn't submitted, try again later"
            return JsonResponse({'message': message, 'error': True})

def submit_email(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            email_msg = request.POST.get('message')
            mail = EmailMessage('Message from {}: {}'.format(name, subject), email_msg, email, [my_user.email], reply_to=[email])
            mail.send()
            # send_mail(subject, email_msg, email, [my_user.email], fail_silently=False)
            message = "Your email was sent successfully, thank you"
            return JsonResponse({'message': message, 'success': True})
        except:
            message = "Email was unsuccessful, try again later"
            return JsonResponse({'message': message, 'error': True})

def get_blog_posts(request):
    blog_api_token = os.environ.get('blog_api_token')
    endpoint = 'http://127.0.0.1:8000/blogposts/api/'
    headers = {
        'Authorization': f'Token {blog_api_token}'
    }
    getting_blog_posts = requests.get(endpoint, headers=headers) 
    gotten_blog_posts  = json.loads(getting_blog_posts.content)
    return JsonResponse({'all_posts': gotten_blog_posts})

def robots_txt(request):
    
    text = [
        "User-agent: *",
        "Disallow: /admin/"
    ]

    return HttpResponse("\n".join(text), content_type = "text/plain")