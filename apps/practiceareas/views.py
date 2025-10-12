from django.shortcuts import render, get_object_or_404
from .models import PracticeArea

# Create your views here.

def practiceareas(request):
    active_slugs = list(PracticeArea.objects.filter(active=True).values_list('slug', flat=True))
    areas_map = {a.slug: a for a in PracticeArea.objects.filter(active=True)}
    return render(request, 'practiceareas/practiceareas.html', {"active_slugs": active_slugs, "areas_map": areas_map})


def derechocivil(request):
    area = get_object_or_404(PracticeArea, slug='derechocivil', active=True)
    active_slugs = list(PracticeArea.objects.filter(active=True).values_list('slug', flat=True))
    return render(request, 'practiceareas/derechocivil.html', {"active_slugs": active_slugs, "area": area})


def derechopenal(request):
    area = get_object_or_404(PracticeArea, slug='derechopenal', active=True)
    active_slugs = list(PracticeArea.objects.filter(active=True).values_list('slug', flat=True))
    return render(request, 'practiceareas/derechopenal.html', {"active_slugs": active_slugs, "area": area})


def derechofamiliar(request):
    area = get_object_or_404(PracticeArea, slug='derechofamiliar', active=True)
    active_slugs = list(PracticeArea.objects.filter(active=True).values_list('slug', flat=True))
    return render(request, 'practiceareas/derechofamiliar.html', {"active_slugs": active_slugs, "area": area})


def derechomercantil(request):
    area = get_object_or_404(PracticeArea, slug='derechomercantil', active=True)
    active_slugs = list(PracticeArea.objects.filter(active=True).values_list('slug', flat=True))
    return render(request, 'practiceareas/derechomercantil.html', {"active_slugs": active_slugs, "area": area})


def derecholaboral(request):
    area = get_object_or_404(PracticeArea, slug='derecholaboral', active=True)
    active_slugs = list(PracticeArea.objects.filter(active=True).values_list('slug', flat=True))
    return render(request, 'practiceareas/derecholaboral.html', {"active_slugs": active_slugs, "area": area})


def derechofiscal(request):
    area = get_object_or_404(PracticeArea, slug='derechofiscal', active=True)
    active_slugs = list(PracticeArea.objects.filter(active=True).values_list('slug', flat=True))
    return render(request, 'practiceareas/derechofiscal.html', {"active_slugs": active_slugs, "area": area})
