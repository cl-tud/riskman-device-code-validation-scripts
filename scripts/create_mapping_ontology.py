"""
This script reads a CSV file containing mappings between GMDN and EMDN codes
with associated confidence scores. It filters mappings with a score above a
given threshold and generates OWL Turtle (`.ttl`) files expressing equivalence
relationships between GMDN and EMDN device classes.

Each accepted mapping results in a triple of the form:

    gmdn:<GMDN_CODE> owl:equivalentClass emdn:<EMDN_CODE> .

For example:

    # GMDN: 10024 <-> EMDN: H900303        
    gmdn:10024 owl:equivalentClass emdn:H900303 .

These triples can be used to align device classification schemes in semantic
reasoning, ontology mapping, or RDF-based integration tasks.

The output also includes the required RDF and OWL prefixes for compatibility
with standard ontology tooling.
"""

import pandas as pd


def generate_turtle_rules(df, threshold):
    turtle_rules = []
    for _, row in df[df['score'] > threshold].iterrows():
        gmdn, emdn = row['GMDN'], row['EMDN']
        rule = f"""
# GMDN: {gmdn} <-> EMDN: {emdn}        
gmdn:{gmdn} owl:equivalentClass emdn:{emdn} .
"""
        turtle_rules.append(rule)
    return "\n".join(turtle_rules)

def get_gmdn_emdn_mapping_ontology(input_mapping_csv, threshold, output_mapping_ttl):
    df = pd.read_csv(input_mapping_csv)
    
    rules = f"""@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix riskman: <https://w3id.org/riskman/ontology#> .
@prefix gmdn: <http://gmdn.org/> .
@prefix emdn: <http://emdn.org/> .
@prefix imdrf: <http://imdrf.org/> .
"""
    rules += generate_turtle_rules(df, threshold)
    
    with open(output_mapping_ttl, 'w') as f:
        f.write(rules)
    
    print(f"Generated {len(df[df['score'] > threshold])} rules in {output_mapping_ttl}")
