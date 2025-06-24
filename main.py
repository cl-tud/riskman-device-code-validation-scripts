"""
Pipeline script to generate ontology mappings and SHACL constraints from 
GMDN–EMDN similarity scores and MAUDE-derived device-patient relationships.

Steps:
1. Convert raw mappings (.txt) to CSV (all + highest-scoring per GMDN)
2. Extract constraints from MAUDE JSON (filtered by count threshold)
3. Generate SHACL constraints (GMDN and EMDN-based)
4. Generate RDF equivalence mappings (if above confidence threshold)

Output is saved in the 'target/' directory.
"""


import os

from scripts import create_mapping_csv, create_csv_constraints, generate_shapes_ttl, get_gmdn_emdn_mapping_ontology


CONFIDENCE_TRESHOLD = 0.8
CONSTRAINT_COUNT_TRESHOLD = 50

# this file is not provided inside the repository
CONSTRAINTS_MAUDE_JSON = 'maude.json'

# input files
MAPPING_NAME = 'fullmapping1'
MAPPING_INPUT_FILE = f'gmdn-emdn-sample-mappings/{MAPPING_NAME}.txt'


# output path 
OUTPUT = 'target'

# interim / output files
MAPPING_CSV_ALL = f'{OUTPUT}/{MAPPING_NAME}_all.csv'
MAPPING_CSV_HIGHEST = f'{OUTPUT}/{MAPPING_NAME}.csv'
OUTPUT_MAPPING_RDF = f'{OUTPUT}/gmdn_emdn_{MAPPING_NAME}.ttl'
# 
CONSTRAINTS_CSV = f'{OUTPUT}/constraints_{MAPPING_NAME}.csv'
CONSTRAINTS_GMDN_TTL = f'{OUTPUT}/constraints_gmdn_{MAPPING_NAME}.ttl'
CONSTRAINTS_EMDN_TTL = f'{OUTPUT}/constraints_emdn_{MAPPING_NAME}.ttl'


if __name__ == '__main__':
    
    os.makedirs(OUTPUT, exist_ok=True)

    create_mapping_csv(MAPPING_INPUT_FILE, MAPPING_CSV_ALL, MAPPING_CSV_HIGHEST)
    create_csv_constraints(MAPPING_CSV_HIGHEST, CONSTRAINTS_MAUDE_JSON, CONSTRAINT_COUNT_TRESHOLD, CONSTRAINTS_CSV)
    generate_shapes_ttl(CONSTRAINTS_CSV, CONSTRAINTS_EMDN_TTL, CONSTRAINTS_GMDN_TTL)
    get_gmdn_emdn_mapping_ontology(MAPPING_CSV_HIGHEST, CONFIDENCE_TRESHOLD, OUTPUT_MAPPING_RDF)



