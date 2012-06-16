from django import template
from datetime import datetime

register = template.Library()

@register.filter
def bubble_color(post_date):
    now = datetime.utcnow()
    then = post_date.replace(tzinfo=None)
    lapsed = now - then
    d = lapsed.days
    style = ['badge-success', 'badge-warning', 'badge-warning', 'badge-important', 'badge-important', 'badge-important', 'badge-inverse']
    #return d
    if d<7:
        return style[d]
    else:
        return 'badge-inverse'
