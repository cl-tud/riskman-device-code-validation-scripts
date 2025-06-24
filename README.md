# Helper scripts for Device Code validation

# IMDRF ontology

### Running
Install python dependencies, by creating a new python environment and execture the `create_imdrf_ontology.py` script
```
python -m venv validation-env
source validation-env/bin/activate
pip install -r requirements.txt
python create_imdrf_ontology.py
```
This will create the `imdrf_ontology.ttl` file in the repository's root directory.

# 

## GMDN–EMDN Mapping and Constraint Generation Pipeline

This repository also provides a data pipeline to generate RDF equivalence mappings between GMDN and EMDN codes and SHACL constraints based on confidence scores from MAUDE data.

### Input Files

- `gmdn-emdn-sample-mappings/{MAPPING_NAME}.txt`: whitespace-separated similarity mappings with no header (GMDN, EMDN, score).
- `maude.json`: external JSON file containing device–patient problem co-occurrence data (not included in the repository).

### Running the Pipeline

To execute the full pipeline:

```bash
python main.py
```

This script:

1. **Creates CSVs** from raw GMDN–EMDN mappings:
   - `{MAPPING_NAME}_all.csv`: all mappings with scores.
   - `{MAPPING_NAME}.csv`: filtered to highest-scoring EMDN per GMDN.

2. **Filters constraints** from `maude.json` using the top GMDN–EMDN mappings and a co-occurrence count threshold.

3. **Generates SHACL constraints**:
   - `constraints_gmdn_*.ttl`: constraints using GMDN codes.
   - `constraints_emdn_*.ttl`: constraints using EMDN codes.

4. **Generates OWL equivalence mappings** (`owl:equivalentClass`) for pairs with a score above the confidence threshold.

All outputs are stored in the `target/` directory.

### Configuration

Adjust the following constants in `main.py` if needed:

```python
CONFIDENCE_TRESHOLD = 0.8
CONSTRAINT_COUNT_TRESHOLD = 50
MAPPING_NAME = 'fullmapping1'  # change to match your input filename
```

Ensure the following input files exist:
- `gmdn-emdn-sample-mappings/fullmapping1.txt`
- `maude.json` (not contained in the repository)
