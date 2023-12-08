from dataclasses import dataclass, field
from typing import Any

from menu.models import Item


@dataclass
class ItemRelation:
    """Keep information about item relations.

    Attributes:
        item (`Item`): the item instance.
        parent (`int` | `None`): the item instance `parent_id` field.
        child (`set[int]`): set of the related items.

    Note:
        Is root if the `parent` field is `None`.
    """

    item: Item
    parent: int | None = None
    child: set[int] = field(default_factory=set)


MenuItemRelations = dict[int, ItemRelation]
Tree = dict[Item, Any | None]
