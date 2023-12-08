from django.template import Library
from django.utils.translation import gettext as _

from menu.models import Item
from menu.typing import Tree


register = Library()


@register.inclusion_tag(
    name="draw_items",
    filename="menu/draw_items.html",
    takes_context=True,
)
def draw_items(context, items: Tree):
    """Draw items tree.

    Returned attributes:
        items (Tree): the items tree.
        active (int): the active item id, sets in the `draw_menu` tag context.
        query (str): the query pattern, sets in the `draw_menu` tag context. 
    """
    return {
        "items": items,

        "active": context.get("active"),
        "query": context.get("query"),
    }


@register.simple_tag(name="query_to_item")
def query_to_item(pattern: str, item: Item):
    """Feels pattern with item id."""
    return pattern % item.id
