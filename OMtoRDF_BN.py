import os
import uuid
import xml.etree.ElementTree as ET
from rdflib import Graph, Namespace, URIRef, BNode, Literal, RDF
from pathlib import Path
from itertools import count

OM = Namespace("http://openmath.org/vocab/math#")
CD = Namespace("http://www.openmath.org/cd/")
EX = Namespace("http://example.org/ontology#")
RDF_NS = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

bnode_counter = count()

def get_unique_uri(suffix=""):
    return URIRef(str(EX) + str(uuid.uuid4()) + suffix)

def new_blank_node():
    return BNode(f"n{next(bnode_counter)}")

def create_variable(g, name):
    var_node = new_blank_node()
    g.add((var_node, RDF.type, OM.Variable))
    g.add((var_node, OM.name, Literal(name)))
    return var_node

def create_literal(g, value):
    lit_node = new_blank_node()
    g.add((lit_node, RDF.type, OM.Literal))
    g.add((lit_node, OM.value, Literal(value)))
    return lit_node

def create_rdf_list(g, elements):
    if not elements:
        return RDF.nil
    first = new_blank_node()
    g.add((first, RDF.first, elements[0]))
    g.add((first, RDF.rest, create_rdf_list(g, elements[1:])))
    return first

def parse_element(elem, g):
    tag = elem.tag.split("}")[-1]

    if tag == "OMV":
        return create_variable(g, elem.attrib["name"])
    elif tag == "OMS":
        return URIRef(str(CD) + elem.attrib["cd"] + "#" + elem.attrib["name"])
    elif tag == "OMI":
        return create_literal(g, int(elem.text))
    elif tag == "OMF":
        return create_literal(g, float(elem.attrib["dec"]))
    elif tag == "OMA":
        app_node = get_unique_uri("_app")
        g.add((app_node, RDF.type, OM.Application))
        children = list(elem)
        operator = parse_element(children[0], g)
        g.add((app_node, OM.operator, operator))
        args = [parse_element(child, g) for child in children[1:]]
        if args:
            list_root = create_rdf_list(g, args)
            g.add((app_node, OM.arguments, list_root))
        return app_node
    else:
        raise ValueError(f"Unknown OpenMath-Tag: {tag}")

def convert_xml_to_ttl(xml_file):
    global bnode_counter
    bnode_counter = count()

    tree = ET.parse(xml_file)
    root = tree.getroot()

    g = Graph()
    g.bind("om", OM)
    g.bind("cd", CD)
    g.bind("ex", EX)
    g.bind("rdf", RDF_NS)

    parse_element(root[0], g)
    g.serialize(destination=xml_file.with_suffix(".ttl"), format="turtle")

if __name__ == "__main__":
    folder = Path(__file__).parent
    for file in folder.glob("*.xml"):
        try:
            convert_xml_to_ttl(file)
            print(f" {file.name} converted.")
        except Exception as e:
            print(f"  Error with {file.name}: {e}")
