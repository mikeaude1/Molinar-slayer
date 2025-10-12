from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.views.decorators.cache import never_cache

from django.contrib.auth.models import User

from .forms import AdminUserCreateForm
from .forms import AdminUserUpdateForm
from .forms import PracticeAreaForm, BlogPostForm, BlogPostEditForm
from .forms import PortalBackgroundForm, AboutUsBackgroundForm
from .forms import BlogArticleFormSet, BlogArticleFormSetEdit
from apps.portal.models import PortalSettings, BlogPost
from apps.practiceareas.models import PracticeArea


def _require_admin(request):
    profile = getattr(request.user, 'profile', None)
    # Permitir acceso a superusuarios, staff de Django o perfiles con rol admin
    if not (request.user.is_authenticated and (getattr(request.user, 'is_superuser', False) or getattr(request.user, 'is_staff', False) or (profile and getattr(profile, 'is_admin', False)))):
        return False
    return True


@login_required
@never_cache
def dashboard(request):
    if not _require_admin(request):
        return HttpResponseForbidden("No autorizado: se requiere perfil de administrador")
    return render(request, 'administrator/dashboard.html')


@login_required
@never_cache
def edit_portal_background(request):
    if not _require_admin(request):
        return HttpResponseForbidden("No autorizado: se requiere perfil de administrador")
    settings_obj = PortalSettings.get_solo()
    if request.method == 'POST':
        form = PortalBackgroundForm(request.POST, request.FILES, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Imagen de fondo del Home actualizada correctamente.")
            return redirect('administrator:portal_bg')
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        form = PortalBackgroundForm(instance=settings_obj)
    return render(request, 'administrator/edit_portal_background.html', {
        'form': form,
        'settings_obj': settings_obj,
    })


@login_required
@never_cache
def edit_aboutus_background(request):
    if not _require_admin(request):
        return HttpResponseForbidden("No autorizado: se requiere perfil de administrador")
    settings_obj = PortalSettings.get_solo()
    if request.method == 'POST':
        form = AboutUsBackgroundForm(request.POST, request.FILES, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Imagen de fondo de 'Acerca de nosotros' actualizada correctamente.")
            return redirect('administrator:aboutus_bg')
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        form = AboutUsBackgroundForm(instance=settings_obj)
    return render(request, 'administrator/edit_aboutus_background.html', {
        'form': form,
        'settings_obj': settings_obj,
    })


@login_required
@never_cache
def users_list(request):
    if not _require_admin(request):
        return HttpResponseForbidden("No autorizado: se requiere perfil de administrador")
    users = User.objects.select_related('profile').all().order_by('username')
    return render(request, 'administrator/users_list.html', {
        'users': users,
    })

@login_required
@never_cache
def users_create(request):
    if not _require_admin(request):
        return HttpResponseForbidden("No autorizado: se requiere perfil de administrador")
    if request.method == 'POST':
        form = AdminUserCreateForm(request.POST, request.FILES)
        if form.is_valid():
            user, profile = form.save()
            messages.success(request, f"Usuario '{user.username}' creado correctamente.")
            return redirect('administrator:users_list')
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        form = AdminUserCreateForm()
    return render(request, 'administrator/users_create.html', {
        'form': form,
    })

@login_required
@never_cache
def users_edit(request, user_id):
    if not _require_admin(request):
        return HttpResponseForbidden("No autorizado: se requiere perfil de administrador")
    from apps.profiles.models import Profile
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('administrator:users_list')
    profile = getattr(user, 'profile', None)
    if profile is None:
        profile = Profile.objects.create(user=user)
    if request.method == 'POST':
        form = AdminUserUpdateForm(request.POST, request.FILES, instance_user=user, instance_profile=profile)
        if form.is_valid():
            form.save()
            messages.success(request, f"Usuario '{user.username}' actualizado correctamente.")
            return redirect('administrator:users_list')
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        form = AdminUserUpdateForm(instance_user=user, instance_profile=profile)
    return render(request, 'administrator/users_edit.html', {
        'form': form,
        'user_obj': user,
    })

@login_required
@never_cache
def users_toggle_active(request, user_id):
    if not _require_admin(request):
        return HttpResponseForbidden("No autorizado: se requiere perfil de administrador")
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('administrator:users_list')
    user.is_active = not user.is_active
    user.save()
    profile = getattr(user, 'profile', None)
    if profile:
        profile.active = user.is_active
        profile.is_active = user.is_active
        profile.save()
    messages.success(request, f"Estado de '{user.username}' cambiado a {'activo' if user.is_active else 'inactivo' }.")
    return redirect('administrator:users_list')

@login_required
@never_cache
def practiceareas_list(request):
    if not _require_admin(request):
        return HttpResponseForbidden("No autorizado: se requiere perfil de administrador")
    areas = PracticeArea.objects.all().order_by('name')
    return render(request, 'administrator/practiceareas_list.html', {"areas": areas})

@login_required
@never_cache
def practiceareas_create(request):
    if not _require_admin(request):
        return HttpResponseForbidden("No autorizado: se requiere perfil de administrador")
    if request.method == 'POST':
        form = PracticeAreaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Área de práctica creada correctamente.")
            return redirect('administrator:practiceareas_list')
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        form = PracticeAreaForm()
    return render(request, 'administrator/practiceareas_create.html', {"form": form})

@login_required
@never_cache
def practiceareas_edit(request, area_id):
    if not _require_admin(request):
        return HttpResponseForbidden("No autorizado: se requiere perfil de administrador")
    try:
        area = PracticeArea.objects.get(pk=area_id)
    except PracticeArea.DoesNotExist:
        messages.error(request, "Área de práctica no encontrada.")
        return redirect('administrator:practiceareas_list')
    if request.method == 'POST':
        form = PracticeAreaForm(request.POST, request.FILES, instance=area)
        if form.is_valid():
            form.save()
            messages.success(request, "Área de práctica actualizada correctamente.")
            return redirect('administrator:practiceareas_list')
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        form = PracticeAreaForm(instance=area)
    return render(request, 'administrator/practiceareas_edit.html', {"form": form, "area": area})

@login_required
@never_cache
def practiceareas_toggle_active(request, area_id):
    if not _require_admin(request):
        return HttpResponseForbidden("No autorizado: se requiere perfil de administrador")
    try:
        area = PracticeArea.objects.get(pk=area_id)
    except PracticeArea.DoesNotExist:
        messages.error(request, "Área de práctica no encontrada.")
        return redirect('administrator:practiceareas_list')
    area.active = not area.active
    area.save(update_fields=['active'])
    messages.success(request, f"Estado de '{area.name}' cambiado a {'activa' if area.active else 'inactiva' }.")
    return redirect('administrator:practiceareas_list')

@login_required
@never_cache
def blog_list(request):
    if not _require_admin(request):
        return HttpResponseForbidden("No autorizado: se requiere perfil de administrador")
    posts = BlogPost.objects.all()
    return render(request, 'administrator/blog_list.html', {"posts": posts})

@login_required
@never_cache
def blog_create(request):
    if not _require_admin(request):
        return HttpResponseForbidden("No autorizado: se requiere perfil de administrador")
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                post = form.save()
                formset = BlogArticleFormSet(request.POST, request.FILES, instance=post)
                if formset.is_valid():
                    formset.save()
                    messages.success(request, "Entrada de blog creada correctamente.")
                    return redirect('administrator:blog_list')
                else:
                    # si el formset falla, revertimos y mostramos errores
                    transaction.set_rollback(True)
                    messages.error(request, "Por favor corrige los errores de los artículos.")
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
        # Si llegamos aquí, necesitamos recrear formset con datos para mostrar errores
        # Nota: si form no es válido, no existe post; usamos instancia vacía
        dummy_post = BlogPost()
        formset = BlogArticleFormSet(request.POST, request.FILES, instance=dummy_post)
    else:
        form = BlogPostForm()
        # instancia vacía solo para construir el formset
        formset = BlogArticleFormSet(instance=BlogPost())
    return render(request, 'administrator/blog_create.html', {"form": form, "formset": formset})

@login_required
@never_cache
def blog_edit(request, post_id):
    if not _require_admin(request):
        return HttpResponseForbidden("No autorizado: se requiere perfil de administrador")
    try:
        post = BlogPost.objects.get(pk=post_id)
    except BlogPost.DoesNotExist:
        messages.error(request, "Entrada no encontrada.")
        return redirect('administrator:blog_list')
    if request.method == 'POST':
        form = BlogPostEditForm(request.POST, request.FILES, instance=post)
        formset = BlogArticleFormSetEdit(request.POST, request.FILES, instance=post)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
                messages.success(request, f"Entrada '{post.title}' actualizada correctamente.")
                return redirect('administrator:blog_list')
        else:
            messages.error(request, "Por favor corrige los errores del formulario o de los artículos.")
    else:
        form = BlogPostEditForm(instance=post)
        formset = BlogArticleFormSetEdit(instance=post)
    return render(request, 'administrator/blog_edit.html', {"form": form, "post": post, "formset": formset})

@login_required
@never_cache
def blog_toggle_active(request, post_id):
    if not _require_admin(request):
        return HttpResponseForbidden("No autorizado: se requiere perfil de administrador")
    try:
        post = BlogPost.objects.get(pk=post_id)
    except BlogPost.DoesNotExist:
        messages.error(request, "Entrada no encontrada.")
        return redirect('administrator:blog_list')
    post.active = not post.active
    post.save(update_fields=['active'])
    messages.success(request, f"Estado de '{post.title}' cambiado a {'activa' if post.active else 'inactiva' }.")
    return redirect('administrator:blog_list')
