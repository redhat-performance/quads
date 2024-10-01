
from dominate import tags
from flask_nav3 import Nav
from flask_nav3.elements import Subgroup
from flask_nav3.renderers import BootStrap5Renderer


class SubMenuNav(Nav):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        submenu_bootstrap5 = SubMenuBootStrap5Renderer
        self._renderers = [("bootstrap5", submenu_bootstrap5)]


class SubMenuBootStrap5Renderer(BootStrap5Renderer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def visit_Subgroup(self, node):
        """Returns subgroup divs."""
        group = tags.ul(_class="dropdown-menu")
        kwargs = {"data-bs-toggle": "dropdown"}
        title = tags.a(
            node.title,
            href="#",
            _class="nav-link dropdown-toggle",
            **kwargs,
        )

        if node.active:
            title.attributes["class"] = "nav-link dropdown-toggle active"

        for item in node.items:
            if isinstance(item, SubMenuGroup):
                group.add(tags.li(self.visit(item), _class="dropdown-item dropdown-submenu"))
            else:
                group.add(tags.li(self.visit(item), _class="dropdown-item"))

        return tags.div(title, group, _class="dropdown")

    def visit_SubMenuGroup(self, node):
        """Returns subMenuGroup divs."""
        group = tags.ul(_class="dropdown-menu")
        kwargs = {"data-bs-toggle": "dropdown"}
        title = tags.a(
            node.title,
            href="#",
            _class="nav-link dropdown-toggle",
            **kwargs,
        )

        if node.active:
            title.attributes["class"] = "nav-link dropdown-toggle active"

        for item in node.items:
            if isinstance(item, SubMenuGroup):
                group.add(tags.li(self.visit(item), _class="dropdown-item dropdown-submenu"))
            else:
                group.add(tags.li(self.visit(item), _class="dropdown-item submenu-item"))

        return tags.span(title, group)


class SubMenuGroup(Subgroup):
    """Nested substructure.

    Usually used to express a submenu.
    """
