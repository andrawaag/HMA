import requests
import pprint
from xml.etree import ElementTree
from bs4 import BeautifulSoup
import xml.dom.minidom
from rdflib import Namespace, Graph, URIRef, BNode, Literal
from rdflib.namespace import DCTERMS, RDFS, RDF, DC, FOAF, SKOS, XSD

HMAGraph = Graph()

#hma = requests.get("http://www.metabolicatlas.org/assets/hmr/HMRcollection2_00.xml-f0de1f951d16f78abf131cece19f8af7.zip")
file = "/Users/andra/Downloads/HMRdatabase2_00.xml"
tree = ElementTree.parse(file)
root = tree.getroot()
print(root.tag)
base = Namespace("http://rdf.hmr.metabolicatlas.org/")
hmap = Namespace(base+"property/")
reactionIRI = Namespace(base+"reaction/")
compartmentIRI = Namespace(base+"compartment/")
speciesIRI = Namespace(base+"species/")

for compartment in tree.iter(tag='{http://www.sbml.org/sbml/level2/version3}compartment'):
    compartmentUri = compartmentIRI[compartment.attrib["id"]]
    HMAGraph.add((compartmentUri, RDF.type, URIRef("http://biomodels.net/SBO/"+compartment.attrib["sboTerm"])))
    HMAGraph.add((compartmentUri, RDFS.label, Literal(compartment.attrib["name"], lang="en")))
    HMAGraph.add((compartmentUri, hmap.hasSpatialDimension, Literal(int(compartment.attrib["spatialDimensions"]), datatype=XSD.integer)))

for species in tree.iter(tag='{http://www.sbml.org/sbml/level2/version3}species'):
    speciesUri = speciesIRI[species.attrib["id"]]
    HMAGraph.add((speciesUri, RDF.type, URIRef("http://biomodels.net/SBO/"+species.attrib["sboTerm"])))
    HMAGraph.add((speciesUri, RDFS.label, Literal(species.attrib["name"], lang="en")))
    HMAGraph.add((speciesUri, DCTERMS.isPartOf, compartmentIRI[species.attrib["compartment"]]))

for reaction in tree.iter(tag='{http://www.sbml.org/sbml/level2/version3}reaction'):
    reactionUri = reactionIRI[reaction.attrib["id"]]
    HMAGraph.add((reactionUri, RDF.type, URIRef("http://biomodels.net/SBO/"+reaction.attrib["sboTerm"])))
    HMAGraph.add((reactionUri, DCTERMS.identifier, Literal(reaction.attrib["id"])))
    #reactants
    for reactantlist in reaction.iter('{http://www.sbml.org/sbml/level2/version3}listOfReactants'):
        for reactant in reactantlist.iter('{http://www.sbml.org/sbml/level2/version3}speciesReference'):
            print(reactant.attrib)
            HMAGraph.add((reactionUri, hmap.hasReactant, speciesIRI[reactant.attrib["species"]]))
    for productlist in reaction.iter('{http://www.sbml.org/sbml/level2/version3}listOfProducts'):
        for product in productlist.iter('{http://www.sbml.org/sbml/level2/version3}speciesReference'):
            print(reactant.attrib)
            HMAGraph.add((reactionUri, hmap.hasProduct, speciesIRI[reactant.attrib["species"]]))
    for modifierslist in reaction.iter('{http://www.sbml.org/sbml/level2/version3}listOfModifiers'):
        for modifier in modifierslist.iter('{http://www.sbml.org/sbml/level2/version3}modifierSpeciesReference'):
            print(reactant.attrib)
            HMAGraph.add((reactionUri, hmap.hasModifier, speciesIRI[reactant.attrib["species"]]))

    # print(BeautifulSoup(tree, "xml").prettify())

HMAGraph.serialize(destination='/tmp/hma.ttl', format='turtle')

#xml = xml.dom.minidom.parse(file) # or xml.dom.minidom.parseString(xml_string)
#pretty_xml_as_string = xml.toprettyxml()
#print(pretty_xml_as_string)
#file = open('/tmp/sbo.xml', 'w')
#file.write(pretty_xml_as_string)
#file.close()