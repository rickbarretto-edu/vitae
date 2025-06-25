
import abc
from xml.dom.minidom import parseString

from vitae.features.ingestion.parsing._xml import Node, parse


__all__ = [
    "XmlString",
    "Document"
]

type XmlString = str

class Document(abc.ABC):

    @property
    @abc.abstractmethod
    def template(self) -> XmlString:
        ...

    @staticmethod
    def of(content: str):
        class Sample(Document):
            @property
            def template(self) -> XmlString:
                return content
            
        return Sample()

    def __str__(self) -> str:
        xml = f"""<?xml version="1.0" ?>
        <CURRICULO-VITAE>
            {self.template}
        </CURRICULO-VITAE>
        """
        return self._formated(xml)
    
    @property
    def as_node(self) -> Node:
        return parse(str(self))
    

    def _formated(self, content: XmlString) -> XmlString:
        return parseString(content).toprettyxml(indent="    ")
        