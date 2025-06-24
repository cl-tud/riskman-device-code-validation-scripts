"""
Reads a whitespace-separated file of GMDN–EMDN similarity scores and outputs:

1. All mappings (`output_all`)
2. One best-scoring EMDN per GMDN (`output_filtered`)

Expected columns: GMDN, EMDN, score (no header).
"""


import pandas as pd


def create_mapping_csv(input_path, output_all, output_filtered):
    df = pd.read_csv(input_path, sep=r'\s+', header=None, 
                     names=['GMDN', 'EMDN', 'score'])
    df.to_csv(output_all, index=False)
    (df.loc[df.groupby('GMDN')['score'].idxmax()]
       .to_csv(output_filtered, index=False))
