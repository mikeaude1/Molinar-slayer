from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Role(models.Model):
    ROLE_ADMIN = 'admin'
    ROLE_LAWYER = 'lawyer'
    ROLE_CLIENT = 'client'
    ROLE_SECRETARY = 'secretary'
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Administrator'),
        (ROLE_LAWYER, 'Lawyer'),
        (ROLE_CLIENT, 'Client'),
        (ROLE_SECRETARY, 'Secretary'),
    ]

    code = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['code']
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # Reemplaza el rol único por múltiples roles
    roles = models.ManyToManyField(Role, blank=True, related_name='profiles')
    phone = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)
    # Imagen de perfil
    image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    practice_areas = models.ManyToManyField('practiceareas.PracticeArea', blank=True, related_name='profiles')
    # Asignación de abogados (solo perfiles con rol "lawyer" podrán ser elegibles vía formularios)
    assigned_lawyers = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='secretaries')
    is_active = models.BooleanField(default=True)

    # Unified 'active' flag for consistency across tables
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['user__username']
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        # Muestra usuario y roles
        roles_display = ', '.join(self.roles.values_list('name', flat=True)) or 'Sin roles'
        return f"{self.user.username} - {roles_display}"

    @property
    def is_admin(self):
        return self.roles.filter(code=Role.ROLE_ADMIN).exists()

    @property
    def is_lawyer(self):
        return self.roles.filter(code=Role.ROLE_LAWYER).exists()

    @property
    def is_client(self):
        return self.roles.filter(code=Role.ROLE_CLIENT).exists()

    @property
    def is_secretary(self):
        return self.roles.filter(code=Role.ROLE_SECRETARY).exists()
