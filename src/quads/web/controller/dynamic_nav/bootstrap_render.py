
from dominate import tags

from quads.web.controller.dynamic_nav.markup_elements import SubMenuGroup


class BootStrapRender:
    """
    A very basic Bootstrap 5 renderer.
    Renders a navigational structure using ``<nav>`` and ``<ul>`` tags that
    can be styled using modern CSS.
    """

    def visit(self, node):
        """
        Visit a node.
        """
        if isinstance(node, type):
            mro = node.mro()
        else:
            mro = type(node).mro()
        for cls in mro:
            meth = getattr(self, 'visit_' + cls.__name__, None)
            if meth is None:
                continue
            return meth(node)

        raise NotImplementedError('No visitation method visit_{}'
                                  .format(node.__class__.__name__))

    def __init__(self, **kwargs):
        """Constructor for ``SimpleRenderer``."""
        self.kwargs = kwargs

    def visit_Link(self, node):
        """Returns hrefs matching url."""
        return tags.a(node.text, href=node.get_url(), _class="nav-link")

    def visit_Navbar(self, node):
        """Returns navbar classes."""
        kwargs = self.kwargs.copy()

        add_class = []
        if "class" in self.kwargs:
            add_class = kwargs["class"].split(" ")

        kwargs["class"] = " ".join(add_class + ["navbar", "navbar-expand-lg"])
        icon = tags.span(_class="navbar-toggler-icon")
        button = tags.button(icon, _class="navbar-toggler btn",
                             _data_bs_toggle="collapse", _data_bs_target="#navbarSupportedContent")
        cont = tags.nav(button, **kwargs)
        ul = cont.add(tags.ul(_id="navbarSupportedContent", _class=" ".join(add_class + ["nav collapse navbar-collapse"])))

        for item in node.items:
            ul.add(tags.li(self.visit(item), _class="nav-item"))

        return cont

    def visit_View(self, node):
        """Returns hrefs."""
        kwargs = {"class": "nav-link"}
        if node.active:
            kwargs["_class"] = "nav-link active"
        return tags.a(
            node.text,
            href=node.get_url(),
            title=node.text,
            **kwargs,
        )  # noqa: WPS221

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

        for item in node.items:
            if isinstance(item, SubMenuGroup):
                group.add(tags.li(self.visit(item), _class="dropdown-item dropdown-submenu"))
            else:
                group.add(tags.li(self.visit(item), _class="dropdown-item"))

        return tags.div(title, group, _class="dropdown")

    def visit_SubMenuGroup(self, node):
        """Returns subMenuGroup divs."""
        group = tags.ul(_class="dropdown-menu")
        kwargs = {}
        title = tags.a(
            node.title,
            href="#",
            _class="nav-link dropdown-toggle menu-title",
            **kwargs,
        )

        for item in node.items:
            if isinstance(item, SubMenuGroup):
                group.add(tags.li(self.visit(item), _class="dropdown-item dropdown-submenu"))
            else:
                group.add(tags.li(self.visit(item), _class="dropdown-item submenu-item"))

        return title, group
