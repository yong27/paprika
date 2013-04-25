from django import template
from django.conf import settings
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(is_safe=True)
def markdown(value, arg=''):
    try:
        import markdown2
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError("Error in 'markdown' filter: The Python markdown2 library isn't installed.")
        return force_text(value)
    else:
        return mark_safe(markdown2.markdown(force_text(value), extras=[
                'fenced-code-blocks', 
                'cuddled-lists', 
                'footnotes', 
                'markdown-in-html', 
                'pyshell', 'smart-pants', 'wiki-tables',
                ]))
