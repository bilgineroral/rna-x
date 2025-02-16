import os
import re
import pandas as pd
from Bio import SeqIO

# File paths
catrapid_file = "data/catrapid_yeast_normalised.txt"  # Protein-RNA interaction file
ncrna_file = "data/ncrna.fa"  # Non-coding RNA FASTA file
cdna_file = "data/cdna.fa"  # Coding RNA FASTA file
output_file = "data/yeast_rna_sequences.fasta"  # Output file with filtered RNA sequences
log_file = "logs/missing_transcripts.log"  # Log file for missing transcripts

# Step 1: Read catRAPID file and extract valid transcript IDs
df = pd.read_csv(catrapid_file, sep="\t")
valid_transcripts = set(df["ensembl_transcript_id"].astype(str).str.strip())  # Strip spaces

# Step 2: Load FASTA sequences into a dictionary with cleaned IDs
fasta_files = [ncrna_file, cdna_file]
fasta_dict = {}

for file in fasta_files:
    for record in SeqIO.parse(file, "fasta"):
        fasta_id = record.id.split()[0]  # Take the first part of the header
        fasta_id = re.sub(r"_.*$", "", fasta_id)  # Remove anything after "_" (handles mRNA, ncRNA variations)
        fasta_dict[fasta_id] = record  # Store sequence under cleaned ID

# Step 3: Filter sequences based on valid transcript IDs
found = 0
missing_transcripts = []

with open(output_file, "w") as out_fasta:
    for transcript_id in valid_transcripts:
        if transcript_id in fasta_dict:
            record = fasta_dict[transcript_id]
            record.seq = record.seq.transcribe()  # Convert T to U (RNA format)
            SeqIO.write(record, out_fasta, "fasta")
            found += 1
        else:
            missing_transcripts.append(transcript_id)

# Step 4: Log missing transcripts
with open(log_file, "w") as log:
    for tid in missing_transcripts:
        log.write(f"{tid}\n")

# Summary Output
print(f"Extraction complete! {found} sequences saved in {output_file}.")
if missing_transcripts:
    print(f"WARNING: {len(missing_transcripts)} transcript IDs were not found in the FASTA files.")
    print(f"Check {log_file} for missing transcript IDs.")

os.remove(ncrna_file)
os.remove(cdna_file)
