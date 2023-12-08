import re

from urllib.parse import urlparse
from django.template import Library
from django.utils.translation import gettext as _

from menu.tree import get_menu_tree


register = Library()


@register.inclusion_tag(
    name="draw_menu",
    filename="menu/draw_menu.html",
    takes_context=True,
)
def draw_menu(context, menu: str):
    """Draw the menu by the given name.

    Returned attributes:
        slug (str): the given menu slug.
        active (int): the active menu item id.
        query (str): the query pattern for menu ids, will be used on the menu
            item render.
        menu (Tree): the menu tree dependent on the active item.
    """
    request = context["request"]
    # If item exists and is digit convert it to integer, set None otherwise.
    active_item = (
        int(item)
        if (item := request.GET.get(menu)) and item.isdigit()
        else None
    )

    # Get the request query and provide menu value
    query = urlparse(request.get_full_path()).query
    pattern = rf"{menu}=\d+"

    if re.search(pattern, query):
        # If menu parameter already exists, replace if with format value
        new_query = re.sub(
            pattern,
            f"{menu}=%d",
            query,
            1,
        )
    else:
        # Just extend with menu parameter otherwise
        new_query = query + f"&{menu}=%d"

    return {
        "slug": menu,
        "active": active_item,
        "query": new_query,
        "menu": get_menu_tree(menu, active_item),
    }
