"""XML parsing helper objects.

Warning:
-------
Never use ``if element`` for ``element: ET.Element``,
this may give you undefined behavior.
Instead, explicitly check if this is ``None``.

"""

from __future__ import annotations

from xml.etree import ElementTree as ET

from src.lib.result import catch

__all__ = ["Node", "ParsingError", "as_int", "attribute", "find"]


class ParsingError(ET.ParseError):
    pass


def normalized(tag: str) -> str:
    return tag.upper().replace(" ", "-")


def find(element: ET.Element | None, tag: str) -> ET.Element | None:
    if element is not None:
        return element.find(normalized(tag))

    return None


def attribute(element: ET.Element | None, tag: str) -> str | None:
    """Get attribute by tag from ET.Element.

    Params
    ------
    element: Node element
    tag: attribute's key

    Returns:
    -------
    Attribute or None

    Note:
    ----
    If an attribute is an empty string,
    it is returned as None for data consistency.

    """
    if element is None:
        return None

    attribute: str | None = element.attrib.get(normalized(tag))
    return attribute.strip() if attribute else None


def as_int(text: str | None) -> int | None:
    if text and text.isdigit():
        return int(text)

    return None


class Node:
    def __init__(self, element: ET.Element | None) -> None:
        self.element = element

    def __getitem__(self, tag: str) -> str | None:
        return attribute(self.element, tag)

    @property
    def exists(self) -> bool:
        return self.element is not None

    def first(self, tag: str) -> Node:
        return Node(find(self.element, tag))

    def all(self, tag: str) -> list[Node]:
        if self.element is None:
            return []
        return [Node(e) for e in self.element.findall(normalized(tag))]


def parse(content: str) -> Node:
    if result := catch(lambda: ET.fromstring(content)):
        return Node(result.value)
    raise ParsingError(result.error) from result.error
