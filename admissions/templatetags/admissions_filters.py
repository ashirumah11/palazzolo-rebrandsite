import re
from django import template

register = template.Library()


@register.filter
def sum_fees(fees):
    """Sum up the amount values from a list of Fee objects."""
    total = 0
    for fee in fees:
        try:
            total += float(fee.amount)
        except (ValueError, TypeError, AttributeError):
            pass
    return total


@register.filter
def format_total(total):
    """Format a total amount as KSh with comma separators."""
    try:
        total = float(total)
        return f"KSh {total:,.0f}"
    except (ValueError, TypeError):
        return "KSh 0"


@register.filter
def safe_slugify(value):
    """Create a URL-safe slug from a value."""
    if not value:
        return ''
    value = str(value)
    value = re.sub(r'[^\w\s-]', '', value).strip()
    value = re.sub(r'[-\s]+', '-', value)
    return value.lower()