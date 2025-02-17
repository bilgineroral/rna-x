import os
from tqdm import tqdm
from Bio import SeqIO

# File paths
catrapid_file = "data/catrapid_yeast_normalised.txt"
rna_fasta_file = "data/yeast_rna_sequences.fasta"
protein_fasta_file = "data/yeast_protein_sequences.fasta"

output_pairs = "data/yeast_rnact.txt"
output_rna = "data/yeast_rna_sequences.txt"
output_protein = "data/yeast_protein_sequences.txt"
error_log_file = "logs/errors.log"

# Load RNA sequences into a dictionary
rna_sequences = {}
print("\nLoading RNA sequences...")
with open(rna_fasta_file, "r") as rna_file:
    for record in SeqIO.parse(rna_file, "fasta"):
        rna_id = record.id.split("_")[0]  # Remove suffixes like _mRNA, _ncRNA
        rna_sequences[rna_id] = str(record.seq)

# Load Protein sequences into a dictionary
protein_sequences = {}
print("\nLoading protein sequences...")
with open(protein_fasta_file, "r") as protein_file:
    for record in SeqIO.parse(protein_file, "fasta"):
        uniprot_id = record.id.split("|")[1]  # Extract Uniprot accession ID
        protein_sequences[uniprot_id] = str(record.seq)

# Initialize missing sets
missing_rna = set()
missing_protein = set()

# Process catRAPID pairs
print("\nProcessing RNA-Protein pairs...")
with open(catrapid_file, "r") as catrapid, open(output_pairs, "w") as pairs_file, open(error_log_file, "w") as error_log:
    next(catrapid)  # Skip header line

    total_lines = sum(1 for _ in open(catrapid_file)) - 1
    catrapid.seek(0)  # Reset file pointer to beginning
    next(catrapid)  # Skip header line again

    # Write header for pairs file
    pairs_file.write("RNA_ID\tProtein_ID\n")

    errors = 0
    with tqdm(total=total_lines, desc="Matching Pairs", unit="pair") as pbar:
        for line in catrapid:
            uniprot_id, ensembl_id, _ = line.strip().split("\t")

            # Check if sequences exist
            if ensembl_id not in rna_sequences:
                missing_rna.add(ensembl_id)
                errors += 1
                continue
            if uniprot_id not in protein_sequences:
                missing_protein.add(uniprot_id)
                errors += 1
                continue

            # Write ID pair instead of sequences
            pairs_file.write(f"{ensembl_id}\t{uniprot_id}\n")
            pbar.update(1)

# Save unique RNA sequences with header
print("\nSaving RNA sequences...")
with open(output_rna, "w") as rna_file:
    rna_file.write("RNA_ID\tRNA_Sequence\n")
    for rna_id, sequence in tqdm(rna_sequences.items(), desc="Writing RNA Sequences"):
        rna_file.write(f"{rna_id}\t{sequence}\n")

# Save unique Protein sequences with header
print("\nSaving Protein sequences...")
with open(output_protein, "w") as protein_file:
    protein_file.write("Protein_ID\tProtein_Sequence\n")
    for protein_id, sequence in tqdm(protein_sequences.items(), desc="Writing Protein Sequences"):
        protein_file.write(f"{protein_id}\t{sequence}\n")

# Log missing sequences with a header
print("\nLogging missing sequences...")
with open(error_log_file, "w") as error_log:
    error_log.write("# Missing Sequences Log\n")
    error_log.write("# RNA_ID or Protein_IDs not found in FASTA files\n")
    for rna_id in missing_rna:
        error_log.write(f"Missing RNA sequence for {rna_id}\n")
    for protein_id in missing_protein:
        error_log.write(f"Missing Protein sequence for {protein_id}\n")

print(f"\nProcessing complete! Outputs:")
print(f"   - Pairs: {output_pairs}")
print(f"   - RNA Sequences: {output_rna}")
print(f"   - Protein Sequences: {output_protein}")
print(f"Could not add {errors} pairs due to missing sequences.")
print(f"Missing sequences logged in {error_log_file}.")

os.remove(rna_fasta_file)
os.remove(protein_fasta_file)
os.remove(catrapid_file)