"""
This script reads a JSON file containing nested device harm data and maps GMDN
codes to EMDN codes using a provided CSV mapping file. For each (GMDN, device
problem, patient problem) combination with a count equal to or above the
specified threshold, it creates a flat CSV record including:

- GMDN code (from JSON)
- Corresponding EMDN code (via mapping CSV)
- Device problem code (from JSON)
- Patient problem code (from JSON)

This allows extraction of medically relevant combinations for further
processing, such as SHACL shape generation or risk analysis.

Example output CSV columns:

    gmdn,emdn,deviceproblem,patientproblem

Example row:

    10089,B0399,A04,E20

Inputs:
- JSON file: nested structure with GMDN → device problems → patient harms
- CSV mapping file: GMDN to EMDN code mappings with optional scores
- Count threshold: filters entries with low occurrence frequency

The script filters data, performs the mapping, and writes the result to a CSV.

Example usage:
    create_csv_constraints('mapping.csv', 'constraints.json', 3, 'output.csv')
"""

import json
import pandas as pd


def process_json_data(json_file, mapping, count_threshold, output_file):
    with open(json_file) as f:
        data = json.load(f)
    
    results = []
    
    for gmdn, gmdn_data in data.items():
        for device_problem, dp_data in gmdn_data.get('devic_p', {}).items():
            for patient_problem, pp_data in dp_data.get('harms', {}).items():
                if pp_data['count'] >= count_threshold:
                    emdn = mapping.get(gmdn, '')  # Empty string if no mapping found
                    results.append({
                        'gmdn': gmdn,
                        'emdn': emdn,
                        'deviceproblem': device_problem,
                        'patientproblem': patient_problem
                    })
    
    # Create DataFrame and save to CSV
    pd.DataFrame(results).to_csv(output_file, index=False)
    print(f"Generated {len(results)} records in {output_file}")


def create_csv_constraints(mapping_file, constraints_json, count_treshold, output_csv):
    mapping_df = pd.read_csv(mapping_file)
    mapping =  dict(zip(mapping_df['GMDN'].astype(str), mapping_df['EMDN']))
    
    process_json_data(constraints_json, mapping, count_treshold, output_csv)
