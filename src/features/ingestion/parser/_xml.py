from xml.etree import ElementTree as ET

from src.lib.result import catch

__all__ = ["Node", "ParsingError", "as_int", "attribute", "find"]


class ParsingError(ET.ParseError):
    pass


def normalized(tag: str) -> str:
    return tag.upper().replace(" ", "-")


def find(element: ET.Element | None, tag: str) -> ET.Element | None:
    if element:
        return element.find(normalized(tag))

    return None


def attribute(element: ET.Element | None, tag: str) -> str | None:
    if element and (element_attribute := element.attrib.get(normalized(tag))):
        return element_attribute.strip()

    return None


def as_int(text: str | None) -> int | None:
    if text and text.isdigit():
        return int(text)

    return None


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
    raise ParsingError(result.error) from result.error
