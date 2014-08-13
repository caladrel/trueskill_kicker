from django import template

register = template.Library()


@register.inclusion_tag('league/state_selector.html', takes_context=True)
def state_selector(context, default, **kwargs):
    current = context['request'].COOKIES.get('m', default)
    current_name = kwargs.get(current, '')
    url = context['request'].get_full_path()

    return {
        'choices': kwargs,
        'current': current,
        'current_name': current_name,
        'url': url
    }

@register.assignment_tag(takes_context=True)
def get_state(context, default):
    return context['request'].COOKIES.get('m', default)
