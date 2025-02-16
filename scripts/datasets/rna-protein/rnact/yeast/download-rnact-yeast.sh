if [ -d "data" ] || [ -d "logs" ]; then
    read -p "data/ and/or logs/ directories already exist. Clear all previous data and download? (y/n) " choice
    case "$choice" in
        y|Y)
            rm -rf data logs
            echo "Cleared existing data directory."
            ;;
        n|N)
            echo "Operation cancelled."
            exit 0
            ;;
        *)
            echo "Operation cancelled."
            exit 1
            ;;
    esac
fi

mkdir data logs

echo "Downloading RNA-protein interactions for yeast from RNAct"
wget -q --show-progress "https://rnact.tartaglialab.com/get?file=catrapid_yeast&type=zip" -O catrapid_yeast.zip
unzip -q catrapid_yeast.zip -d data
rm catrapid_yeast.zip

echo "Downloading all cDNA and ncRNA sequences of yeast from Ensembl"
wget -q --show-progress https://ftp.ensembl.org/pub/current_fasta/saccharomyces_cerevisiae/ncrna/Saccharomyces_cerevisiae.R64-1-1.ncrna.fa.gz
gunzip -q Saccharomyces_cerevisiae.R64-1-1.ncrna.fa.gz

wget -q --show-progress https://ftp.ensembl.org/pub/current_fasta/saccharomyces_cerevisiae/cdna/Saccharomyces_cerevisiae.R64-1-1.cdna.all.fa.gz
gunzip -q Saccharomyces_cerevisiae.R64-1-1.cdna.all.fa.gz

echo "Downloading the reference proteome of yeast from Uniprot"
wget -q --show-progres https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Eukaryota/UP000002311//UP000002311_559292.fasta.gz
gunzip -q UP000002311_559292.fasta.gz

mv Saccharomyces_cerevisiae.R64-1-1.ncrna.fa data/ncrna.fa
mv Saccharomyces_cerevisiae.R64-1-1.cdna.all.fa data/cdna.fa
mv UP000002311_559292.fasta data/proteome.fasta

python extract-uniprot.py
python extract-ensembl.py

python prepare-yeast-dataset.py

echo "Dataset is saved in the data/ directory. Please refer to the README for more information."
