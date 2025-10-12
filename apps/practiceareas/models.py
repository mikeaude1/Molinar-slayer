from django.db import models

# Create your models here.

class PracticeArea(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True)
    description = models.TextField(blank=True)
    # Añadir imagen opcional para el área de práctica
    image = models.ImageField(upload_to='practiceareas/', blank=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Practice Area"
        verbose_name_plural = "Practice Areas"

    def __str__(self):
        return self.name
