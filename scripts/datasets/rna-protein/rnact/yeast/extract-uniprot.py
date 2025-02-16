from Bio import SeqIO
import pandas as pd
import os

fasta_file = "data/proteome.fasta"
output_file = "data/yeast_protein_sequences.fasta"
input_ids_file = "data/catrapid_yeast_normalised.txt"

# Step 1: Read UniProt IDs from input file
df = pd.read_csv(input_ids_file, sep="\t")
uniprot_ids = set(df["uniprot_accession"].tolist())

print(f"Found {len(uniprot_ids)} unique UniProt accession IDs in RNAct database.")

# Step 2: Extract only needed sequences
count = 0
with open(output_file, "w") as out_fasta:
    for record in SeqIO.parse(fasta_file, "fasta"):
        uniprot_acc = record.id.split("|")[1]  # Extract UniProt ID
        if uniprot_acc in uniprot_ids:
            SeqIO.write(record, out_fasta, "fasta")
            count += 1

print(f"Saved {count} yeast sequences to {output_file}")

if count != len(uniprot_ids):
    print(f"Failed to extract the sequences of {len(uniprot_ids) - count} entries")

print(f"Sequences are saved in {output_file}")

os.remove(fasta_file)