"""
This script generates SHACL NodeShapes in Turtle (`.ttl`) format for both GMDN
and EMDN codes based on a CSV input containing medical device classification
mappings and related problems.

Each input row must have:
- `gmdn`: a GMDN code
- `emdn`: corresponding EMDN code
- `deviceproblem`: an IMDRF device problem code
- `patientproblem`: an IMDRF patient problem code

For each row, two SHACL NodeShapes are generated:
1. A GMDN-based shape that checks if the presence of a device problem implies a patient problem, unless explicitly excluded.
2. A parallel EMDN-based shape with the same logic but for the EMDN concept.

The SHACL shapes assert conditional logic on RDF data involving:
- Device classification (`gmdn:<code>` or `emdn:<code>`)
- IMDRF device and patient problems
- Constraints over multiple paths like `riskman:hasControlledRisk`, `riskman:hasPatientProblem`, etc.

Output:
- Two `.ttl` files containing SHACL constraints, one for GMDN and one for EMDN
- Standard RDF prefixes are included at the top

Usage:
    generate_shapes_ttl('input.csv', 'emdn_shapes.ttl', 'gmdn_shapes.ttl')

Typical use case:
This script is part of a pipeline for automatically deriving SHACL constraints
from structured risk data and device classification mappings in the medical
domain, useful for semantic validation or reasoning in RDF-based systems.
"""


import csv


# Template for SHACL shapes
SHACL_TEMPLATE = """@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix dc: <http://purl.org/dc/terms/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <http://ex.org/> .
@prefix riskman: <https://w3id.org/riskman/ontology#> .
@prefix gmdn: <http://gmdn.org/> .
@prefix emdn: <http://emdn.org/> .
@prefix imdrf: <http://imdrf.org/> .

{shapes}"""

SHAPE_TEMPLATE = """
# {comment}
ex:Shape_{code}_{device_problem}_{patient_problem}_{code_type}
    a sh:NodeShape ;
    sh:targetClass riskman:RMF ;
    sh:or (
        [ sh:not [ sh:and (
                    [ sh:property [ sh:path riskman:code;  sh:class {code_prefix}:{code}; ] ]
                    [ sh:property [ sh:path (riskman:hasControlledRisk 
                                             riskman:hasAnalyzedRisk 
                                             riskman:hasDomainSpecificHazard 
                                             riskman:hasDeviceProblem); 
									                  sh:qualifiedValueShape  [ sh:class imdrf:{device_problem} ];
                                    sh:qualifiedMinCount 1
                                  ]
                    ]
                         )
                ]
        ]
      	[ sh:property [ sh:path (riskman:hasControlledRisk  riskman:hasAnalyzedRisk ) ;
                        sh:qualifiedValueShape [ sh:node [ sh:and (
								            [ sh:path (riskman:hasDomainSpecificHazard riskman:hasDeviceProblem); sh:class imdrf:{device_problem} ]
                            [ sh:path riskman:hasPatientProblem; sh:class imdrf:{patient_problem} ]
                                                        )
                                               ] ];
                            sh:qualifiedMinCount 1
                      ]
        ]
      );
    sh:message "If device has {code_prefix} {code} and device problem {device_problem}, then patient problem {patient_problem} must be present" ;
    sh:severity sh:Warning ;
.
"""


def generate_shapes(csv_file):
    shapes_emdn = []
    shapes_gmdn = []
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            
            
            # Generate GMDN shape
            shapes_gmdn.append(SHAPE_TEMPLATE.format(
                comment=f"GMDN: {row['gmdn']}, Device: {row['deviceproblem']}, Patient: {row['patientproblem']}",
                code=row['gmdn'],
                device_problem=row['deviceproblem'],
                patient_problem=row['patientproblem'],
                code_type='GMDN',
                code_prefix='gmdn'
            ))
            
            # Generate EMDN shape
            shapes_emdn.append(SHAPE_TEMPLATE.format(
                comment=f"EMDN: {row['emdn']}, Device: {row['deviceproblem']}, Patient: {row['patientproblem']}",
                code=row['emdn'],
                device_problem=row['deviceproblem'],
                patient_problem=row['patientproblem'],
                code_type='EMDN',
                code_prefix='emdn'
            ))
    
    return SHACL_TEMPLATE.format(shapes=''.join(shapes_gmdn)), SHACL_TEMPLATE.format(shapes=''.join(shapes_emdn))


# Example usage
def generate_shapes_ttl(csv_shapes, output_emdn_ttl_file, output_gmdn_ttl_file):
    gmdn_shacl, emdn_shacl = generate_shapes(csv_shapes)
    
    # Save to file or print
    with open(output_emdn_ttl_file, 'w') as f:
        f.write(emdn_shacl)
        
    with open(output_gmdn_ttl_file, 'w') as f:
        f.write(gmdn_shacl)
    
    print("SHACL constraints generated successfully!")