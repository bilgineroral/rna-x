# RNAct - Yeast (Saccharomyces Cerevisiae)

> **Important**: Run all scripts at this directory level.

To download binding RNA-protein pairs of yeast (S. Cerevisiae) from RNAct, simply type:
```
bash download-rnact-yeast.sh
```
Make sure dependencies are installed (`requirements.txt`).

1. **download-rnact-yeast.sh**
    This script downloads the RNA-protein pairs of yeast from RNAct database, and saves it in `yeast-rnact.txt`. The RNAct provides the file `catrapid_yeast_normalised.txt`, which have the following format:
    ```
    uniprot_accession	ensembl_transcript_id	catrapid_score_max_normalised
    A0A023PYF4	YML009W-B	16.840
    A0A023PYF4	YDL014W	16.510
    ```
    It runs the following python scripts: `extract-ensembl.py`, `extract-uniprot.y` and `prepare-yeast-dataset.py`.

2. **extract-ensembl.py**
    This script creates a file named `yeast_rna_sequences.fasta` to filter downloaded cDNA/ncRNA sequences to include only those who have entries in `catrapid_yeast_normalised.txt` and converts cDNA/ncRNA sequences into RNA sequences (T to U conversion).

    > **Note:** There are 7,029 unique Ensembl Transcript IDs in the `catrapid_yeast_normalised.txt` file, but 107 of them can't be found in the downloaded cDNA or ncRNA FASTA files. These are saved in `missing_transcripts.log` for reference. They're intentionally left out in the final dataset for now.

3. **extract-uniprot.py**
    This script creates a file named `yeast_protein_sequences.fasta` to filter downloaded protein sequences to include only those who have entries in `catrapid_yeast_normalised.txt`.

4. **prepare-yeast-dataset.py**
    This script creates the final dataset file `yeast-rnact.txt`. This file consists of binding RNA and protein IDs. It also creates `yeast_protein_sequences.txt` and `yeast_rna_sequences.txt` files, which consists of RNA/Protein ID - sequence mappings.