from django.shortcuts import render, get_object_or_404
from .models import BlogPost, Testimonial

# Create your views here.
def index(request):
    return render(request, 'portal/index.html')

def aboutus(request):
    return render(request, 'portal/aboutus.html')

def blog_list(request):
    posts = BlogPost.objects.filter(published=True)
    testimonials = Testimonial.objects.filter(published=True)[:6]
    return render(request, 'portal/blog_list.html', {"posts": posts, "testimonials": testimonials})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    testimonials = Testimonial.objects.filter(published=True)[:6]
    return render(request, 'portal/blog_detail.html', {"post": post, "testimonials": testimonials})

