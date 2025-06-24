import json
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, OWL

JSON_FILES = [
    'imdrf/annexa2025_0.JSON',
    'imdrf/annexb2025_0.JSON',
    'imdrf/annexc2025_0.JSON',
    'imdrf/annexd2025_1.JSON',
    'imdrf/annexe2025_0.JSON',
    'imdrf/annexf2025_0.JSON',
    'imdrf/annexg2025_0.JSON',
]

OUTPUT_FILE = "imdrf_ontology.ttl"


def create_ontology(json_files, output_file):
    # Initialize RDF Graph
    g = Graph()
    
    # Define namespaces
    IMDRF = Namespace("http://imdrf.org/")
    ex = Namespace("http://example.org/ontology/")
    
    g.bind("imdrf", IMDRF)
    g.bind("ex", ex)
    g.bind("owl", OWL)
    
    for json_file in json_files:
        with open(json_file, 'r') as f:
            data = json.load(f)
            
            for entry in data:
                # Create class for each code
                class_uri = IMDRF[entry["code"]]
                g.add((class_uri, RDF.type, OWL.Class))
                g.add((class_uri, RDFS.label, Literal(entry["term"])))
                g.add((class_uri, RDFS.comment, Literal(entry["definition"])))
                
                # Add hierarchy if exists
                if "|" in entry["codehierarchy"]:
                    parent_code = entry["codehierarchy"].split("|")[-2]
                    parent_uri = IMDRF[parent_code]
                    g.add((class_uri, RDFS.subClassOf, parent_uri))
                
                # Add additional properties
                if entry["non-IMDRF code"]:
                    g.add((class_uri, ex.nonIMDRFCode, Literal(entry["non-IMDRF code"])))
                if entry["status"]:
                    g.add((class_uri, ex.status, Literal(entry["status"])))
                if entry["status description"]:
                    g.add((class_uri, ex.statusDescription, Literal(entry["status description"])))
    
    # Serialize and save the ontology
    g.serialize(destination=output_file, format="turtle")
    print(f"Ontology saved to {output_file}")

# Example usage
if __name__ == "__main__":
    create_ontology(JSON_FILES, OUTPUT_FILE)