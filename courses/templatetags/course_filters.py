from django import template

register = template.Library()


@register.filter
def course_type(courses, course_type):
    """Filter courses by course_type ('full' or 'short')."""
    return [c for c in courses if c.course_type == course_type]