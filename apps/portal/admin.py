from django.contrib import admin
from .models import BlogPost, Testimonial, PortalSettings, BlogArticle

# Register your models here.

class BlogArticleInline(admin.TabularInline):
    model = BlogArticle
    extra = 1
    fields = ("order", "title", "content", "image_url", "image")

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "published", "active", "created_at")
    list_filter = ("published", "active", "created_at")
    search_fields = ("title", "excerpt")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [BlogArticleInline]

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("client_name", "rating", "published", "active", "created_at")
    list_filter = ("published", "active", "rating")
    search_fields = ("client_name", "company", "content")

@admin.register(PortalSettings)
class PortalSettingsAdmin(admin.ModelAdmin):
    list_display = ("id", "updated_at")

admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
