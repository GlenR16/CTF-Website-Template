from django import template
import uuid
import random

register = template.Library()

@register.simple_tag
def random_string():
    return uuid.uuid4().hex[:random.randint(27,32)]*random.randint(10,25)