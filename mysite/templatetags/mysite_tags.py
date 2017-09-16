from django import template
from django.utils.safestring import mark_safe
from django.conf import settings
import os
import random

register = template.Library()


@register.simple_tag
def load_background():
    image_show_count = 6  # cannot be larger than the amount of images
    curdir = os.path.join(settings.MEDIA_ROOT, "background")
    items = os.listdir(curdir)
    selected = [items[i] for i in random.sample(range(len(items)), image_show_count)]
    urls = ["/media/background/{}".format(x) for x in selected]

    return mark_safe("""
        <section class="hidden-xs">
            <ul class="cb-slideshow">
                <li><span style="background-image: url('{}')"></span></li>
                <li><span style="background-image: url('{}')"></span></li>
                <li><span style="background-image: url('{}')"></span></li>
                <li><span style="background-image: url('{}')"></span></li>
                <li><span style="background-image: url('{}')"></span></li>
                <li><span style="background-image: url('{}')"></span></li>
            </ul>
        </section>
    """.format(*urls))
