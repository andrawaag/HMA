from SPARQLWrapper import SPARQLWrapper, JSON
import pprint

sboQuery = """
   PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX dbpedia2: <http://dbpedia.org/property/>
PREFIX dbpedia: <http://dbpedia.org/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?class ?label ?description
FROM <http://rdf.ebi.ac.uk/dataset/sbo>
   WHERE {
       ?class rdfs:subClassOf* <http://biomodels.net/SBO/SBO_0000375> ;
              rdfs:comment ?description ;
              rdfs:label ?label .
   }
"""
sparql = SPARQLWrapper("https://www.ebi.ac.uk/rdf/services/sparql")
sparql.setQuery(sboQuery)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
pprint.pprint(results)
for result in results["results"]["bindings"]:
    print("CREATE")
    print("LAST\tLen\t\""+result["label"]["value"]+"\"")
    print("LAST\tDen\t\"Term from the Systems Biology Ontology\"")
    print("LAST\tP31\tQ1969448")
    print("LAST\tP361\tQ2377160")
    print("LAST\tP2888\t\""+result["class"]["value"]+"\"")