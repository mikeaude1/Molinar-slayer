from django.shortcuts import render, get_object_or_404
from .models import BlogPost, Testimonial, PortalSettings
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse
from apps.profiles.forms import CaptchaAuthenticationForm
from apps.practiceareas.models import PracticeArea

# Create your views here.
def index(request):
    settings_obj = PortalSettings.get_solo()
    testimonials = Testimonial.objects.filter(published=True, active=True)[:6]
    active_slugs = list(PracticeArea.objects.filter(active=True).values_list('slug', flat=True))
    ordered_slugs = ['derechocivil','derechopenal','derechofamiliar','derechomercantil','derecholaboral','derechofiscal']
    first_three = [slug for slug in ordered_slugs if slug in active_slugs][:3]
    label_map = {
        'derechocivil': 'Derecho Civil',
        'derechopenal': 'Derecho Penal',
        'derechofamiliar': 'Derecho Familiar',
        'derechomercantil': 'Derecho Mercantil/Corporativo',
        'derecholaboral': 'Derecho Laboral',
        'derechofiscal': 'Derecho Fiscal',
    }
    image_map = {
        'derechocivil': 'images/derechocivil.jpg',
        'derechopenal': 'images/derechopenal.jpg',
        'derechofamiliar': 'images/derechofamiliar.jpg',
        'derechomercantil': 'images/derechomercantil.jpg',
        'derecholaboral': 'images/derecholaboral.jpg',
        'derechofiscal': 'images/derechofiscal.jpg',
    }
    featured_areas = [{"slug": slug, "label": label_map.get(slug, slug), "image": image_map.get(slug), "url": reverse(f'practiceareas:{slug}')} for slug in first_three]
    return render(request, 'portal/index.html', {"portal_settings": settings_obj, "testimonials": testimonials, "active_slugs": active_slugs, "featured_areas": featured_areas})


def aboutus(request):
    settings_obj = PortalSettings.get_solo()
    return render(request, 'portal/aboutus.html', {"portal_settings": settings_obj})


def blog_list(request):
    posts = BlogPost.objects.filter(published=True, active=True)
    return render(request, 'portal/blog_list.html', {"posts": posts})


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, published=True, active=True)
    articles = post.articles.all().order_by('order', 'created_at')
    return render(request, 'portal/blog_detail.html', {"post": post, "articles": articles})


class PortalLoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = CaptchaAuthenticationForm

    def form_invalid(self, form):
        if form.errors.get('__all__'):
            messages.error(self.request, 'Credenciales inválidas. Verifica usuario y contraseña.')
        if form.errors.get('hcaptcha'):
            messages.error(self.request, 'La verificación hCaptcha falló. Intenta nuevamente.')
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, 'Inicio de sesión exitoso.')
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user
        if getattr(user, 'is_superuser', False) or getattr(user, 'is_staff', False):
            return reverse('administrator:dashboard')
        profile = getattr(user, 'profile', None)
        if profile and getattr(profile, 'is_admin', False):
            return reverse('administrator:dashboard')
        if profile and getattr(profile, 'is_lawyer', False):
            return reverse('profiles:lawyer_dashboard')
        return reverse('profiles:dashboard')

