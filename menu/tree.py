from dataclasses import asdict
from typing import Iterable

from menu.models import Item
from menu.typing import ItemRelation, MenuItemRelations, Tree


def get_item_relations(menu: str) -> MenuItemRelations:
    """Create menu item relations dictionary.

    Returns the parent and child items related with an item using
    `ItemRelation` class.

    Args:
        menu: the specific menu name.
    """
    items = Item.objects.all().select_related('menu').filter(menu__slug=menu)

    item_relations: MenuItemRelations = {}

    for item in items:
        parent_id = getattr(item, 'parent_id')

        # If item parent is None, then create or update `ItemRelation` instance
        # Return existed properties dict, if the instance already
        item_relations[item.pk] = ItemRelation(
            # exists, otherwise - empty dict
            **(
                asdict(item_relation)
                if (item_relation := item_relations.get(item.pk))
                else {}
            ),
            item=item,
            parent=parent_id,
        )

        if not parent_id:
            continue

        # Handle item parent relation
        # - create parent `ItemRelation` instance if missing
        # - update `child` set if exists

        parent_item_relation = item_relations.get(parent_id)

        # Create instance if not exists
        if not parent_item_relation:
            # An empty value means that this `Item` instance will be handled
            # later, so i can use temporary value for that will be overwritten
            item_relations[parent_id] = ItemRelation(
                item=Item(title='__temp__'),
            )
            parent_item_relation = item_relations[parent_id]

        parent_item_relation.child.add(item.pk)

    return item_relations


def get_relations_roots(
    relations: MenuItemRelations,
) -> Iterable[ItemRelation]:
    """Return root menu items."""
    return filter(lambda value: value.parent is None, relations.values())


def get_menu_root_tree(relations: MenuItemRelations) -> Tree:
    """Create tree from the root menu items sequence.

    Sets `None` value for all root menu item.
    """
    return {
        relations_root_item.item: None
        for relations_root_item in get_relations_roots(relations)
    }


def create_tree(relations: MenuItemRelations, item_id: int | None = None) -> Tree:
    """Create menu tree dependent in active item.

    Returns the tree of the menu root items if the active item id was not
    specified.

    Args:
        relations: the menu item relations.
        item_id: the active menu item id, can be None.
    """
    def fill_tree(relation: ItemRelation, tree_part: Tree | None) -> Tree:
        """Recursively fills the menu tree.

        Args:
            relation: current item relation.
            tree_part: the tree part related with the current item.
        """
        # Base case.
        # Missing item parent means that this item is root.
        # So get other root items to show all available routes and complete
        # the recursion.
        if not relation.parent:
            relations_root = get_menu_root_tree(relations)
            relations_root[relations[relation.item.pk].item] = tree_part
            return relations_root

        # Recursion step.
        # Get parent item relations, set the current item value as the given
        # `tree_part` and `None` for other child items.
        # Continue to full tree.
        parent_relation = relations[relation.parent]
        return fill_tree(
            parent_relation,
            {
                relations[child].item: (
                    tree_part
                    if child == relation.item.pk
                    else None
                )
                for child in parent_relation.child
            },
        )

    # If item id was not provided, return tree from menu root items
    if item_id is None or relations.get(item_id) is None:
        return get_menu_root_tree(relations)

    # Get active chat relations
    item_relation = relations[item_id]

    # Fill active item child with `None` value
    base = (
        {relations[child].item: None for child in item_relation.child}
        if item_relation.child
        else None
    )

    return fill_tree(item_relation, base)


def get_menu_tree(menu: str, child: int | None = None):
    """Create menu tree with provided menu and active child.

    Args:
        menu: the specific menu name.
        child: the active child id, can be None.
    """
    return create_tree(get_item_relations(menu), child)
