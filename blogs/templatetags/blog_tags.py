from urllib.parse import urlencode, urlparse, parse_qs
from django.utils.safestring import mark_safe
from django import template
from django.conf import settings
import os


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


@register.simple_tag
def emoticon_bar():
    cur_dir = os.path.join(settings.MEDIA_ROOT, "emoticon")
    emoticon_set_names = [x for x in os.listdir(cur_dir) if os.path.isdir(os.path.join(cur_dir, x))]
    emoticon_dirs = [os.path.join(cur_dir, x) for x in emoticon_set_names]
    tab_list = ""
    img_list = ""
    for set_ind, emoticon_set_name in enumerate(emoticon_set_names):
        emoticon_dir = os.path.join(cur_dir, emoticon_set_name)
        files = [x for x in os.listdir(emoticon_dir) if os.path.isfile(os.path.join(emoticon_dir, x))]
        urls = [settings.MEDIA_URL + "emoticon/{}/{}".format(emoticon_set_name, x) for x in files]

        img_list = ""
        for ind, url in enumerate(urls):
            img_list += """<img src="{}" data-ind={}>""".format(url, ind)
        cur_set = """
        <div class="emoticon-img" data-emoticon_set_name="{emoticon_set_name}">
            {img_str}
        </div>
        """.format(emoticon_set_name=emoticon_set_name, img_str=img_list)
        tab_list += """
        <li data-ind={set_ind} data-selected="0"><div>{set_name}</div></li>
        """.format(set_ind=set_ind, set_name=emoticon_set_name)

    string = """
    <div class="emoticon-div">
        <div class="emoticon-tab">
            {tab_list}
        </div>
        {img_list}
    </div>
    """.format(tab_list=tab_list, img_list=cur_set)
    return mark_safe(string)
