import json
import os
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.mail import send_mail, EmailMessage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.templatetags.static import static
from .models import Portfolio, Tool, Feedback, ProfessionalExperience, Education, Summary, Service, Project, ProjectCategory


User = get_user_model()

# Create your views here.
def index(request):
    cache_key = "portfolio_index_data"
    context = cache.get(cache_key)



    if not context:
        try:
            my_portfolio = Portfolio.objects.select_related("user").prefetch_related("services").get(user__username="Victor")
        except Portfolio.DoesNotExist:
            # handle missing portfolio gracefully
            return render(request, "my_portfolio/index.html", {})
        
        my_user = my_portfolio.user
        email = my_user.email

        tools = Tool.objects.all()
        feedbacks = Feedback.objects.select_related().all()
        all_experience = ProfessionalExperience.objects.all().order_by('-id')
        summary = Summary.objects.select_related("user").get(user=my_user)
        education = Education.objects.all().order_by('-id')
        services = Service.objects.all()
        projects = Project.objects.filter(user=my_user).select_related("category").prefetch_related("tools", "projectthumbnail").order_by('-date')
        project_categories = ProjectCategory.objects.all()

        context = {
            'email': email,
            "tools": tools,
            "feedbacks": feedbacks,
            "all_experience": all_experience,
            "summary": summary,
            "education": education,
            "services": services,
            'my_portfolio': my_portfolio,
            "projects": projects,
            "project_categories": project_categories,
        }

        # Cache for 10 minutes
        cache.set(cache_key, context, 600)

    return render(request, "my_portfolio/index.html", context)



    


def project_detail(request, slug):
    # cache key specific to this project
    cache_key = f"project_detail_{slug}"
    cached_data = cache.get(cache_key)

    if cached_data:
        return render(request, 'my_portfolio/project-details.html', cached_data)

    project = get_object_or_404(Project.objects.select_related('category', 'user').prefetch_related('tools', 'projectthumbnail'), slug=slug)
    
    # Get thumbnail efficiently
    project_thumbnail = project.projectthumbnail.first()
    thumbnail_url = project_thumbnail.image.url if project_thumbnail else static("og-image.png")
    
    context = {
        'project': project,
        'project_thumbnail': project_thumbnail,
        'thumbnail_url': thumbnail_url,
        # Add breadcrumb data for better UX
        'breadcrumb': {
            'home': 'Home',
            'projects': 'Projects',
            'current': project.title
        }
    }

    # Cache for 30 minutes (projects don't change frequently)
    cache.set(cache_key, context, 1800)


    return render(request, 'my_portfolio/project-details.html', context)

def submit_feedback(request):
    if request.method == 'POST':
        # Verify reCAPTCHA first
        recaptcha_response = request.POST.get('g-recaptcha-response')

        if not recaptcha_response:
            return JsonResponse({'message': 'CAPTCHA verification required', 'error': True})
        
        try:
            # Verify with Google
            data = {
                'secret': settings.RECAPTCHA_SECRET_KEY,  # From Google Console
                'response': recaptcha_response
            }
            
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            
            if not result.get('success'):
                return JsonResponse({'message': 'CAPTCHA verification failed', 'error': True})
        except:
            return JsonResponse({'message': 'Verification service unavailable. Please try again.', 'error': True})

        try:
            my_user = User.objects.filter(username='Victor').first()
            name =request.POST.get('name')
            email = request.POST.get('email')
            feedback = request.POST.get('message')
            image = request.FILES.get('image')
            Feedback.objects.create(name=name, email=email, feedback=feedback, image=image)
            message = 'Your feedback was sent, thank you'
            send_mail('New feedback message from {}'.format(name), feedback, email, [my_user.email], fail_silently=True)
            return JsonResponse({'message': message, 'success': True})
        except:
            message = "Feedback wasn't submitted, try again later"
            return JsonResponse({'message': message, 'error': True})

def submit_email(request):
    my_user = User.objects.filter(username='Victor').first()
    if request.method == 'POST':
        # Verify reCAPTCHA
        recaptcha_response = request.POST.get('g-recaptcha-response')
        if not recaptcha_response:
            return JsonResponse({'message': 'CAPTCHA verification required', 'error': True})
        
        try:
            data = {
                'secret': settings.RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data, timeout=10)
            result = r.json()
            
            if not result.get('success'):
                return JsonResponse({'message': 'CAPTCHA verification failed', 'error': True})
            
            # Process email if CAPTCHA passes
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = f"Message from {name}"
            email_msg = request.POST.get('message')
            mail = EmailMessage('Message from {}: {}'.format(name, subject), email_msg, email, [my_user.email], reply_to=[email])
            mail.send()
            message = "Your email was sent successfully, thank you"
            return JsonResponse({'message': message, 'success': True})
            
        except requests.RequestException:
            return JsonResponse({'message': 'Verification service unavailable', 'error': True})
        except Exception:
            return JsonResponse({'message': 'Email was unsuccessful, try again later', 'error': True})

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
        "Disallow: /portfolioadmin/"
    ]

    return HttpResponse("\n".join(text), content_type = "text/plain")