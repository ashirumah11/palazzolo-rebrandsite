from django import template

register = template.Library()


@register.filter
def get_choice_display(choices, key):
    """Get the display value for a choice key from a list of (value, label) tuples."""
    if not choices:
        return ''
    choices_dict = dict(choices)
    return choices_dict.get(key, '')