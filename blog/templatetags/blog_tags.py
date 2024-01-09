from django import template
from ..models import Post
from django.db.models import Count
register=template.Library()
from django.utils.safestring import mark_safe
import markdown





@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag('blog/latest.html')

def show_latest(count=5):
    latest=Post.published.order_by('-publish')[:count]
    return {'latest':latest}



@register.simple_tag
def most_commented(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))