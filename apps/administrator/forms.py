from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from apps.profiles.models import Profile, Role
from apps.practiceareas.models import PracticeArea
from apps.portal.models import BlogPost, BlogArticle
from apps.portal.models import PortalSettings


def ensure_default_roles():
    """Crea los roles básicos si no existen."""
    defaults = [
        (Role.ROLE_ADMIN, 'Administrator'),
        (Role.ROLE_LAWYER, 'Lawyer'),
        (Role.ROLE_CLIENT, 'Client'),
        (Role.ROLE_SECRETARY, 'Secretary'),
    ]
    for code, name in defaults:
        Role.objects.get_or_create(code=code, defaults={'name': name})


class AdminUserCreateForm(forms.Form):
    username = forms.CharField(label="Usuario", max_length=150)
    email = forms.EmailField(label="Email", required=False)
    first_name = forms.CharField(label="Nombre", max_length=150, required=False)
    last_name = forms.CharField(label="Apellidos", max_length=150, required=False)

    roles = forms.ModelMultipleChoiceField(
        label="Roles",
        queryset=Role.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    image = forms.ImageField(label="Imagen de perfil", required=False)

    phone = forms.CharField(label="Teléfono", max_length=30, required=False)
    bio = forms.CharField(label="Biografía", widget=forms.Textarea, required=False)

    practice_areas = forms.ModelMultipleChoiceField(
        label="Áreas de práctica",
        queryset=PracticeArea.objects.filter(active=True),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    assigned_lawyers = forms.ModelMultipleChoiceField(
        label="Asignar abogado",
        queryset=Profile.objects.none(),
        required=False,
        widget=forms.SelectMultiple,
    )

    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    active = forms.BooleanField(label="Activo", required=False, initial=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ensure_default_roles()
        self.fields['roles'].queryset = Role.objects.order_by('code')
        # Solo abogados en el selector
        self.fields['assigned_lawyers'].queryset = Profile.objects.filter(is_active=True, roles__code=Role.ROLE_LAWYER).select_related('user').order_by('user__username')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Este nombre de usuario ya existe.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError("Este email ya está en uso.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise ValidationError("Las contraseñas no coinciden.")
        roles = cleaned.get('roles') or []
        role_codes = set([r.code for r in roles])
        # Áreas de práctica: solo si tiene rol abogado
        if Role.ROLE_LAWYER not in role_codes and cleaned.get('practice_areas'):
            self.add_error('practice_areas', "Solo los perfiles con rol 'Abogado' pueden tener áreas de práctica.")
        # Asignación de abogado: requerido si rol cliente o secretaria
        if (Role.ROLE_CLIENT in role_codes or Role.ROLE_SECRETARY in role_codes) and not cleaned.get('assigned_lawyers'):
            self.add_error('assigned_lawyers', "Debe asignar al menos un abogado si el usuario es cliente o secretaria.")
        return cleaned

    def save(self):
        data = self.cleaned_data
        user = User(
            username=data['username'],
            email=data.get('email') or "",
            first_name=data.get('first_name') or "",
            last_name=data.get('last_name') or "",
            is_active=data.get('active', True),
        )
        user.set_password(data['password1'])
        user.save()

        profile = Profile(
            user=user,
            phone=data.get('phone') or "",
            bio=data.get('bio') or "",
            is_active=data.get('active', True),
            active=data.get('active', True),
        )
        # Imagen
        image = data.get('image')
        if image:
            profile.image = image
        profile.save()
        # Roles
        roles = data.get('roles') or []
        profile.roles.set(roles)
        # Áreas de práctica (solo si tiene rol abogado)
        role_codes = set([r.code for r in roles])
        if Role.ROLE_LAWYER in role_codes and data.get('practice_areas'):
            profile.practice_areas.set(data['practice_areas'])
        else:
            profile.practice_areas.clear()
        # Asignación de abogados (si cliente o secretaria)
        if (Role.ROLE_CLIENT in role_codes or Role.ROLE_SECRETARY in role_codes) and data.get('assigned_lawyers'):
            profile.assigned_lawyers.set(data['assigned_lawyers'])
        else:
            profile.assigned_lawyers.clear()
        return user, profile


class AdminUserUpdateForm(forms.Form):
    username = forms.CharField(label="Usuario", max_length=150)
    email = forms.EmailField(label="Email", required=False)
    first_name = forms.CharField(label="Nombre", max_length=150, required=False)
    last_name = forms.CharField(label="Apellidos", max_length=150, required=False)

    roles = forms.ModelMultipleChoiceField(
        label="Roles",
        queryset=Role.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    image = forms.ImageField(label="Imagen de perfil", required=False)

    phone = forms.CharField(label="Teléfono", max_length=30, required=False)
    bio = forms.CharField(label="Biografía", widget=forms.Textarea, required=False)
    practice_areas = forms.ModelMultipleChoiceField(
        label="Áreas de práctica",
        queryset=PracticeArea.objects.filter(active=True),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    assigned_lawyers = forms.ModelMultipleChoiceField(
        label="Asignar abogado",
        queryset=Profile.objects.none(),
        required=False,
        widget=forms.SelectMultiple,
    )

    # Edición opcional de contraseña
    password1 = forms.CharField(label="Nueva contraseña", widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label="Confirmar nueva contraseña", widget=forms.PasswordInput, required=False)

    active = forms.BooleanField(label="Activo", required=False)

    def __init__(self, *args, **kwargs):
        self.instance_user = kwargs.pop('instance_user', None)
        self.instance_profile = kwargs.pop('instance_profile', None)
        super().__init__(*args, **kwargs)
        ensure_default_roles()
        self.fields['roles'].queryset = Role.objects.order_by('code')
        self.fields['assigned_lawyers'].queryset = Profile.objects.filter(is_active=True, roles__code=Role.ROLE_LAWYER).select_related('user').order_by('user__username')
        if self.instance_user and self.instance_profile:
            self.fields['username'].initial = self.instance_user.username
            self.fields['email'].initial = self.instance_user.email
            self.fields['first_name'].initial = self.instance_user.first_name
            self.fields['last_name'].initial = self.instance_user.last_name

            # Inicializar roles múltiples
            self.fields['roles'].initial = self.instance_profile.roles.all()
            self.fields['phone'].initial = self.instance_profile.phone
            self.fields['bio'].initial = self.instance_profile.bio
            self.fields['practice_areas'].initial = self.instance_profile.practice_areas.all()
            self.fields['assigned_lawyers'].initial = self.instance_profile.assigned_lawyers.all()
            self.fields['active'].initial = self.instance_profile.active and self.instance_user.is_active

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if self.instance_user:
            qs = qs.exclude(pk=self.instance_user.pk)
        if qs.exists():
            raise ValidationError("Este nombre de usuario ya existe.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            return email
        qs = User.objects.filter(email=email)
        if self.instance_user:
            qs = qs.exclude(pk=self.instance_user.pk)
        if qs.exists():
            raise ValidationError("Este email ya está en uso.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 or p2:
            if not p1 or not p2 or p1 != p2:
                raise ValidationError("Las contraseñas no coinciden.")
        roles = cleaned.get('roles') or []
        role_codes = set([r.code for r in roles])
        # Áreas de práctica: solo si tiene rol abogado
        if Role.ROLE_LAWYER not in role_codes and cleaned.get('practice_areas'):
            self.add_error('practice_areas', "Solo los perfiles con rol 'Abogado' pueden tener áreas de práctica.")
        # Asignación de abogado: requerido si rol cliente o secretaria
        if (Role.ROLE_CLIENT in role_codes or Role.ROLE_SECRETARY in role_codes) and not cleaned.get('assigned_lawyers'):
            self.add_error('assigned_lawyers', "Debe asignar al menos un abogado si el usuario es cliente o secretaria.")
        return cleaned

    def save(self):
        data = self.cleaned_data
        user = self.instance_user
        profile = self.instance_profile
        user.username = data['username']
        user.email = data.get('email') or ""
        user.first_name = data.get('first_name') or ""
        user.last_name = data.get('last_name') or ""
        user.is_active = data.get('active', True)
        # Cambiar contraseña si se proporcionó
        if data.get('password1'):
            user.set_password(data['password1'])
        user.save()

        # Imagen
        image = data.get('image')
        if image:
            profile.image = image
        # Roles y otros campos
        roles = data.get('roles') or []
        profile.roles.set(roles)
        profile.phone = data.get('phone') or ""
        profile.bio = data.get('bio') or ""
        profile.is_active = data.get('active', True)
        profile.active = data.get('active', True)
        profile.save()
        # Áreas de práctica (solo si tiene rol abogado)
        role_codes = set([r.code for r in roles])
        if Role.ROLE_LAWYER in role_codes and data.get('practice_areas'):
            profile.practice_areas.set(data['practice_areas'])
        else:
            profile.practice_areas.clear()
        # Asignación de abogados (si cliente o secretaria)
        if (Role.ROLE_CLIENT in role_codes or Role.ROLE_SECRETARY in role_codes) and data.get('assigned_lawyers'):
            profile.assigned_lawyers.set(data['assigned_lawyers'])
        else:
            profile.assigned_lawyers.clear()
        return user, profile


class PracticeAreaForm(forms.ModelForm):
    class Meta:
        model = PracticeArea
        fields = ["name", "slug", "description", "image", "active"]


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = [
            "title",
            "slug",
            "excerpt",
            "content",
            "image_url",
            "image",
            "published",
            "active",
        ]

class BlogPostEditForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = [
            "title",
            "slug",
            "image_url",
            "image",
            "published",
            "active",
        ]

# --- Nuevo: formularios para artículos del blog ---
class BlogArticleForm(forms.ModelForm):
    class Meta:
        model = BlogArticle
        fields = ["order", "title", "content", "image_url", "image"]
        widgets = {
            "order": forms.HiddenInput(),
            "title": forms.TextInput(attrs={"placeholder": "Título (opcional)"}),
            "content": forms.Textarea(attrs={"placeholder": "Contenido del artículo"}),
            "image_url": forms.URLInput(attrs={"placeholder": "URL de imagen (opcional)"}),
        }

BlogArticleFormSet = inlineformset_factory(
    BlogPost,
    BlogArticle,
    form=BlogArticleForm,
    fields=["order", "title", "content", "image_url", "image"],
    extra=2,
    can_delete=True,
)

# Formset específico para edición (sin formularios extra por defecto)
BlogArticleFormSetEdit = inlineformset_factory(
    BlogPost,
    BlogArticle,
    form=BlogArticleForm,
    fields=["order", "title", "content", "image_url", "image"],
    extra=0,
    can_delete=True,
)


class PortalBackgroundForm(forms.ModelForm):
    class Meta:
        model = PortalSettings
        fields = ["home_bg"]
        labels = {"home_bg": "Imagen de fondo (Home)"}

class AboutUsBackgroundForm(forms.ModelForm):
    class Meta:
        model = PortalSettings
        fields = ["about_bg"]
        labels = {"about_bg": "Imagen de fondo (Acerca de nosotros)"}