#!/usr/bin/env python3

import argparse
import pandas as pd
import matplotlib.pyplot as plt

TAX_LEVELS = {
    "phylum" : "|p__",
    "class" : "|c__",
    "order" : "|o__",
    "family" : "|f__",
    "genus" : "|g__",
    "species" : "|s__"
}
LEVEL_DEPTH = {
    "phylum": 1,
    "class": 2,
    "order": 3,
    "family": 4,
    "genus": 5,
    "species": 6
}

def get_tax_level(df, level):
    depth = LEVEL_DEPTH[level]
    prefix = TAX_LEVELS[level]

    level_df = df[
        (df["clade_name"].str.contains(prefix, regex=False)) &
        (df["clade_name"].str.count(r"\|") == depth)
    ].copy()

    level_df["label"] = level_df["clade_name"].str.split(prefix).str[-1]
    return level_df

import matplotlib.pyplot as plt


def plot_taxonomy(df, level, top_n=10, out_png=None):
    tax_df = get_tax_level(df, level)
    tax_df = tax_df.sort_values("relative_abundance", ascending=False).head(top_n)

    plt.figure(figsize=(8, 5))
    plt.bar(
        tax_df["clade_name"].str.replace(
        rf".*\{TAX_LEVELS[level]}",
        "",
        regex=True
    ),
        tax_df["relative_abundance"]
    )

    plt.xticks(rotation=90)
    plt.xlabel(level.capitalize())
    plt.ylabel("Relative abundance (%)")
    plt.title(f"Sample - Top {level.capitalize()} Composition")
    plt.tight_layout()

    if out_png:
        plt.savefig(out_png, dpi=300)
    else:
        plt.show()

    plt.close()

import sys
import pandas as pd

def main():
    if len(sys.argv) < 3:
        print("Usage: python metaphlan_plot.py <profile.txt> <level>")
        print("Levels: phylum, class, order, family, genus, species")
        sys.exit(1)

    infile = sys.argv[1]
    level = sys.argv[2]

    if level not in TAX_LEVELS:
        print(f"Invalid level: {level}")
        print("Valid levels:", ", ".join(TAX_LEVELS.keys()))
        sys.exit(1)

    df = pd.read_csv(
        infile,
        sep="\t",
        comment="#"
    )

    df["relative_abundance"] = pd.to_numeric(
        df["relative_abundance"], errors="coerce"
    )

    plot_taxonomy(
        df,
        level=level,
        top_n=10,
        out_png=f"{level}_barplot.png"
    )

if __name__ == "__main__":
    main()

def parse_args():
    parser = argparse.ArgumentParser(
        description="Plot MetaPhlAn taxonomic profiles"
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="MetaPhlAn profile.tsv file"
    )
    parser.add_argument(
        "-l", "--level",
        required=True,
        choices=["phylum", "class", "order", "family", "genus", "species"],
        help="Taxonomic level"
    )
    parser.add_argument(
        "-o", "--output",
        default="output.png",
        help="Output PNG file"
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=10,
        help="Top N taxa"
    )
    return parser.parse_args()

def main():
    args = parse_args()

    df = pd.read_csv(args.input, sep="\t", comment="#")
    plot_taxonomy(
        df,
        level=args.level,
        top_n=args.top_n,
        out_png=args.output
    )

if __name__ == "__main__":
    main()