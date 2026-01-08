# MetaPhlAn Plot Tool

A simple CLI tool to visualize MetaPhlAn taxonomic profiles.

This tool expects a MetaPhlAn profile output where the header line does NOT start with #.
Default MetaPhlAn output (NOT accepted): #clade_name	NCBI_tax_id	relative_abundance	additional_species

Required format (accepted)
Before running metaphlanplot, remove the leading # from the header line:
clade_name	NCBI_tax_id	relative_abundance	additional_species

## Installation

```bash
pip install pandas matplotlib

python metaphlanplot/cli.py \
  --input profile.tsv \
  --level genus \
  --top-n 10 \
  --output genus.png
  
  Supported levels

phylum

class

order

family

genus

species