from xml.etree import ElementTree as ET

from src.lib.result import catch


__all__ = ["Node", "find", "attribute", "as_int", "ParsingError"]


class ParsingError(ET.ParseError):
    pass


def normalized(tag: str) -> str:
    return tag.upper().replace(" ", "-")


def find(element: ET.Element | None, tag: str) -> ET.Element | None:
    if element is None:
        return None

    return element.find(normalized(tag))


def attribute(element: ET.Element | None, tag: str) -> str | None:
    if element is None:
        return None

    if element_attribute := element.attrib.get(normalized(tag)):
        return element_attribute.strip()


def as_int(text: str | None) -> int | None:
    if text is None:
        return None

    if text.isdigit():
        return int(text)


class Node:
    def __init__(self, element: ET.Element | None):
        self.element = element

    def __getitem__(self, tag: str) -> str | None:
        return attribute(self.element, tag)

    @property
    def exists(self) -> bool:
        return self.element is not None

    def first(self, tag: str) -> "Node":
        return Node(find(self.element, tag))

    def all(self, tag: str) -> list["Node"]:
        if self.element is None:
            return []
        return [Node(e) for e in self.element.findall(normalized(tag))]


def parse(content: str) -> Node:
    if result := catch(lambda: ET.fromstring(content)):
        return Node(result.value)
    else:
        raise ParsingError(result.error) from result.error
