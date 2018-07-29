from copy import copy
from lxml import etree


class Schema:
    def __init__(self, schemafile):
        self.root = etree.parse(schemafile)
        self.schema_space = self.root.getroot().nsmap

    def replace_ns(self, path):
        for ns_prefix, ns_uri in self.schema_space.items():
            if ns_prefix:
                path = path.replace(f"{ns_prefix}:", f"{{{ns_uri}}}")
        return path

    def findall(self, path):
        return self.root.findall(self.replace_ns(path))

    def find(self, path):
        return self.root.find(self.replace_ns(path))

    def names_of(self, nodes):
        return [node.get("name") for node in nodes]

    def get_Types(self, t_name):
        return self.names_of(self.findall(t_name))

    def get_simpleTypes(self):
        return self.get_Types("xs:simpleType")

    def get_complexTypes(self):
        return self.get_Types("xs:complexType")

    def get_elements_of_attribute(self, attribute):
        return self.names_of(self.findall(".//xs:element/xs:complexType/xs:" + attribute + "/../.."))

    def get_element_attributes(self, name):
        node = self.find(".//xs:element[@name='" + name + "']")
        if node is None:
            node = self.find(".//xs:complexType[@name='" + name + "']")

        if node is None:
            return None
        else:
            return node.attrib
