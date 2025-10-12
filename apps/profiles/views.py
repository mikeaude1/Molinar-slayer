from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

@login_required
def lawyer_dashboard(request):
    profile = getattr(request.user, 'profile', None)
    # Solo accesible para abogados y administradores
    if not (profile and (profile.is_lawyer or profile.is_admin)):
        return HttpResponseForbidden("No autorizado: se requiere rol abogado o administrador")
    return render(request, 'profiles/lawyer_dashboard.html')

@login_required
def profile_dashboard(request):
    """Panel principal para usuarios autenticados que no sean admin ni abogado.
    Si el usuario es admin/staff o abogado, redirige a sus paneles específicos.
    """
    profile = getattr(request.user, 'profile', None)
    if getattr(request.user, 'is_superuser', False) or getattr(request.user, 'is_staff', False) or (profile and getattr(profile, 'is_admin', False)):
        return redirect('administrator:dashboard')
    if profile and getattr(profile, 'is_lawyer', False):
        return redirect('profiles:lawyer_dashboard')
    return render(request, 'profiles/general_dashboard.html')

# Hacer que logout funcione sin requerir autenticación y redirija correctamente al índice
def logout_view(request):
    """Cerrar sesión y redirigir al inicio mostrando un mensaje en español."""
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    # Redirigir al inicio con i18n hacia la página principal
    return redirect('index')

@login_required
def lawyer_clients(request):
    profile = getattr(request.user, 'profile', None)
    if not (profile and (profile.is_lawyer or profile.is_admin)):
        return HttpResponseForbidden("No autorizado: se requiere rol abogado o administrador")
    return render(request, 'profiles/lawyer_clients.html')

@login_required
def lawyer_cases(request):
    profile = getattr(request.user, 'profile', None)
    if not (profile and (profile.is_lawyer or profile.is_admin)):
        return HttpResponseForbidden("No autorizado: se requiere rol abogado o administrador")
    return render(request, 'profiles/lawyer_cases.html')

@login_required
def lawyer_agenda(request):
    profile = getattr(request.user, 'profile', None)
    if not (profile and (profile.is_lawyer or profile.is_admin)):
        return HttpResponseForbidden("No autorizado: se requiere rol abogado o administrador")
    return render(request, 'profiles/lawyer_agenda.html')

@login_required
def lawyer_invoices_pending(request):
    profile = getattr(request.user, 'profile', None)
    if not (profile and (profile.is_lawyer or profile.is_admin)):
        return HttpResponseForbidden("No autorizado: se requiere rol abogado o administrador")
    return render(request, 'profiles/lawyer_invoices_pending.html')

@login_required
def lawyer_invoices_paid(request):
    profile = getattr(request.user, 'profile', None)
    if not (profile and (profile.is_lawyer or profile.is_admin)):
        return HttpResponseForbidden("No autorizado: se requiere rol abogado o administrador")
    return render(request, 'profiles/lawyer_invoices_paid.html')
