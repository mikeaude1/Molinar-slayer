from django.db import models
from django.utils.translation import get_language

# Create your models here.

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    excerpt = models.TextField(blank=True)
    content = models.TextField()
    image_url = models.URLField(blank=True)
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Campos bilingües (opcionalmente rellenados)
    title_es = models.CharField(max_length=200, blank=True)
    title_en = models.CharField(max_length=200, blank=True)
    excerpt_es = models.TextField(blank=True)
    excerpt_en = models.TextField(blank=True)
    content_es = models.TextField(blank=True)
    content_en = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    # Propiedades de visualización según idioma activo con fallback
    def _current_lang(self):
        lang = get_language() or 'es'
        return (lang[:2]).lower()

    def _pick(self, base_name):
        lang = self._current_lang()
        # Prioridad: campo del idioma activo -> inglés -> español -> legado
        val_lang = getattr(self, f"{base_name}_{lang}", None)
        if val_lang:
            return val_lang
        val_en = getattr(self, f"{base_name}_en", None)
        if val_en:
            return val_en
        val_es = getattr(self, f"{base_name}_es", None)
        if val_es:
            return val_es
        # Fallback al campo original monolingüe
        return getattr(self, base_name, '')

    @property
    def title_display(self):
        return self._pick('title')

    @property
    def excerpt_display(self):
        return self._pick('excerpt')

    @property
    def content_display(self):
        return self._pick('content')


class Testimonial(models.Model):
    client_name = models.CharField(max_length=150)
    content = models.TextField()
    # Campos bilingües para contenido del testimonio
    content_es = models.TextField(blank=True)
    content_en = models.TextField(blank=True)
    rating = models.PositiveSmallIntegerField(default=5)
    company = models.CharField(max_length=150, blank=True)
    avatar_url = models.URLField(blank=True)
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.client_name} ({self.rating}/5)"

    # Propiedad de visualización según idioma con fallback
    @property
    def content_display(self):
        lang = get_language() or 'es'
        lang = (lang[:2]).lower()
        val_lang = getattr(self, f"content_{lang}", None)
        if val_lang:
            return val_lang
        if self.content_en:
            return self.content_en
        if self.content_es:
            return self.content_es
        return self.content
