from django.contrib import admin
from .models import BlogPost, Testimonial

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "published", "created_at")
    list_filter = ("published", "created_at")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "excerpt", "content", "title_es", "title_en", "excerpt_es", "excerpt_en", "content_es", "content_en")

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("client_name", "rating", "published", "created_at")
    list_filter = ("published", "rating")
    search_fields = ("client_name", "company", "content", "content_es", "content_en")
