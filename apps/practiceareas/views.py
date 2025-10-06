from django.shortcuts import render

# Create your views here.

def practiceareas(request):
    return render(request, 'practiceareas/practiceareas.html')


def derechocivil(request):
    return render(request, 'practiceareas/derechocivil.html')


def derechopenal(request):
    return render(request, 'practiceareas/derechopenal.html')


def derechofamiliar(request):
    return render(request, 'practiceareas/derechofamiliar.html')


def derechomercantil(request):
    return render(request, 'practiceareas/derechomercantil.html')


def derecholaboral(request):
    return render(request, 'practiceareas/derecholaboral.html')


def derechofiscal(request):
    return render(request, 'practiceareas/derechofiscal.html')
