from django.contrib import admin
from django.utils.html import format_html

from .models import Course, Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'name', 'duration_months', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'requirements')
    readonly_fields = ('image_preview', 'created_at', 'updated_at')
    fields = ('name', 'description', 'requirements', 'duration_months', 'image', 'image_preview', 'created_at', 'updated_at')

    @admin.display(description='Image')
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height: 100px; width: 150px; object-fit: cover; border-radius: 5px;"/>',
                obj.image.url,
            )
        return 'No image selected'


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'title', 'department', 'course_type_badge', 'specialization', 'duration_months', 'is_active')
    list_filter = ('is_active', 'department', 'course_type', 'specialization')
    search_fields = ('title', 'slug', 'description')
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ('department',)
    readonly_fields = ('image_preview', 'created_at')
    fields = ('title', 'slug', 'department', 'image', 'image_preview', 'course_type', 'specialization', 'duration_months', 'duration_weeks', 'credits', 'description', 'is_active', 'created_at')

    @admin.display(description='Image')
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height: 100px; width: 150px; object-fit: cover; border-radius: 5px;"/>',
                obj.image.url,
            )
        return 'No image uploaded'

    @admin.display(description='Type')
    def course_type_badge(self, obj):
        from django.utils.html import format_html
        colors = {
            'full': 'warning',
            'short': 'success',
        }
        color = colors.get(obj.course_type, 'secondary')
        return format_html(
            '<span class="badge badge-{}">{}</span>',
            color,
            obj.get_course_type_display()
        )
