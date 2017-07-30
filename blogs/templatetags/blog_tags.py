from urllib.parse import urlencode, urlparse, parse_qs
from django import template


register = template.Library()
@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    origin_ajax_url = context.get('origin_ajax_url')
    # if the url is an ajax call
    if origin_ajax_url:
        schema = urlparse(origin_ajax_url)
        query = parse_qs(schema.query)
        # only get the first value
        for key, value in query.items():
            query[key] = value[0]
        query.update(kwargs)
        res_url = schema.path + '?' + urlencode(query)
        return res_url
    else:
        query = context['request'].GET.dict()
        query.update(kwargs)
        return urlencode(query)
