from django import template
from rango.models import Category

register = template.Library()

@register.inclusion_tag('rango/cats.html') #mash up rango/cats.html with a method called get_category_list() which contains all categories
def get_category_list(cat=None):
    print(cat)
    return {'cats':Category.objects.all(),
    'act_cat':cat} #cat does not update its value to the current category being visited
